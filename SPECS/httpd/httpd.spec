Summary:        The Apache HTTP Server
Name:           httpd
Version:        2.4.51
Release:        3%{?dist}
License:        Apache License 2.0
URL:            http://httpd.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://apache.mirrors.hoobly.com/%{name}/%{name}-%{version}.tar.bz2
%define sha1    %{name}=d8ae02630f836d7cf60e24f4676e633518f16e2b

# Patch0 is taken from:
# https://www.linuxfromscratch.org/patches/blfs/svn/httpd-2.4.47-blfs_layout-1.patch
Patch0:         httpd-%{version}-blfs-layout.patch
Patch1:         httpd-uncomment-ServerName.patch

BuildRequires:  openssl >= 1.1.1
BuildRequires:  openssl-devel >= 1.1.1
BuildRequires:  pcre-devel
BuildRequires:  apr
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  openldap
BuildRequires:  expat-devel
BuildRequires:  lua-devel
BuildRequires:  nghttp2-devel

Requires:       nghttp2
Requires:       pcre
Requires:       apr-util
Requires:       openssl >= 1.1.1
Requires:       openldap
Requires:       lua
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

Provides:       apache2

%define _confdir %{_sysconfdir}

%description
The Apache HTTP Server.

%package devel
Summary:    Header files for httpd
Group:      Applications/System
Requires:   httpd

%description devel
These are the header files of httpd.

%package docs
Summary:    Help files for httpd
Group:      Applications/System
Requires:   httpd

%description docs
These are the help files of httpd.

%package tools
Group:      System Environment/Daemons
Summary:    Tools for httpd

%description tools
The httpd-tools of httpd.

%prep
%autosetup -p1

%build
sh ./configure --host=%{_host} --build=%{_build} \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --program-prefix= \
    --disable-dependency-tracking \
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_confdir}/httpd/conf \
    --datadir=%{_sysconfdir}/httpd \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir}/httpd/modules \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-authnz-fcgi \
    --enable-mods-shared="all cgi" \
    --enable-mpms-shared=all \
    --with-apr=%{_prefix} \
    --with-apr-util=%{_prefix} \
    --enable-layout=RPM \
    --enable-http2

GCCVERSION=$(gcc --version | grep ^gcc | sed 's/^.* //g')
$(dirname $(gcc -print-prog-name=cc1))/install-tools/mkheaders

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm755 %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}/etc/httpd/logs

cat << EOF >> %{buildroot}/usr/lib/systemd/system/httpd.service
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/run/httpd/httpd.pid
ExecStart=/usr/sbin/httpd -k start
ExecStop=/usr/sbin/httpd -k stop
ExecReload=/usr/sbin/httpd -k graceful

[Install]
WantedBy=multi-user.target

EOF

install -vdm755 %{buildroot}/usr/lib/systemd/system-preset
echo "disable httpd.service" > %{buildroot}/usr/lib/systemd/system-preset/50-httpd.preset

ln -s /usr/sbin/httpd %{buildroot}/usr/sbin/apache2
ln -s /etc/httpd/conf/httpd.conf %{buildroot}/etc/httpd/httpd.conf

mkdir -p %{buildroot}%{_libdir}/tmpfiles.d
cat >> %{buildroot}%{_libdir}/tmpfiles.d/httpd.conf << EOF
d /run/httpd 0755 root root -
EOF

%post
/sbin/ldconfig
if [ $1 -eq 1 ]; then
  # this is initial installation
  if ! getent group apache >/dev/null; then
    groupadd -g 25 apache
  fi

  if ! getent passwd apache >/dev/null; then
    useradd -c "Apache Server" -d /srv/www -g apache \
        -s /bin/false -u 25 apache
  fi

  if [ -h /etc/mime.types ]; then
    mv /etc/mime.types /etc/mime.types.orig
  fi
fi

ln -sf /etc/httpd/conf/mime.types /etc/mime.types
systemd-tmpfiles --create httpd.conf
%systemd_post httpd.service

%preun
%systemd_preun httpd.service

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  # this is delete operation
  if getent passwd apache >/dev/null; then
    userdel apache
  fi

  if getent group apache >/dev/null; then
    groupdel apache
  fi

  if [ -f /etc/mime.types.orig ]; then
    mv /etc/mime.types.orig /etc/mime.types
  fi
fi
%systemd_postun_with_restart httpd.service

%files devel
%defattr(-,root,root)
%{_includedir}/*

%files docs
%defattr(-,root,root)
%{_sysconfdir}/httpd/manual/*

%files
%defattr(-,root,root)
%{_libdir}/httpd/*
%{_bindir}/*
%exclude %{_bindir}/apxs
%exclude %{_bindir}/dbmmanage
%{_sbindir}/*
%{_datadir}/*
%{_sysconfdir}/httpd/html/index.html
%{_sysconfdir}/httpd/cgi-bin/*
%{_sysconfdir}/httpd/conf/extra
%{_sysconfdir}/httpd/conf/original
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%{_sysconfdir}/httpd/conf/envvars
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%{_sysconfdir}/httpd/conf/mime.types
%{_sysconfdir}/httpd/error/*
%{_sysconfdir}/httpd/icons/*
%{_sysconfdir}/httpd/httpd.conf
%{_libdir}/systemd/system/httpd.service
%{_libdir}/systemd/system-preset/50-httpd.preset
%{_libdir}/tmpfiles.d/httpd.conf
%{_localstatedir}/log/httpd

%files tools
%defattr(-,root,root)
%{_bindir}/apxs
%{_bindir}/dbmmanage

%changelog
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.51-3
- Bump up release for openssl
* Mon Nov 08 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.51-2
- Enable mod_http2
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.51-1
- Version upgrade to fix CVE-2021-42013
* Thu Oct 07 2021 Dweep Advani <dadvani@vmware.com> 2.4.50-1
- Upgraded to 2.4.50 for fixing CVE-2021-41524 and CVE-2021-41773
* Wed Sep 29 2021 Dweep Advani <dadvani@vmware.com> 2.4.49-1
- Upgraded to 2.4.49 for addressing multiple CVEs
* Mon Sep 13 2021 Nitesh Kumar <kunitesh@vmware.com> 2.4.47-2
- Replacement of ITS suggested words.
* Fri May 21 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.47-1
- Bump to v2.4.47
* Tue Mar 23 2021 Piyush Gupta <gpiyush@vmware.com> 2.4.46-6
- Internal version bump up in order to compile with new lua.
* Wed Jan 20 2021 Tapas Kundu <tkundu@vmware.com> 2.4.46-5
- Fix pid path
* Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.4.46-4
- Fix GCC path issue
* Mon Oct 05 2020 Dweep Advani <dadvani@vmware.com> 2.4.46-3
- Create /var/run/httpd temp folder through systemd-tmpfiles
* Tue Sep 01 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.46-2
- Make openssl 1.1.1 compatible
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.46-1
- Automatic Version Bump
* Mon Sep 30 2019 Shreyas B. <shreyasb@vmware.com> 2.4.41-1
- Upgrading to 2.4.41 to address following CVEs.
- (1) CVE-2019-10092 (2) CVE-2019-10098 (3) CVE-2019-10082
- (4) CVE-2019-10081 (5) CVE-2019-9517
* Tue Apr 16 2019 Dweep Advani <dadvani@vmware.com> 2.4.39-1
- Upgrading to 2.4.39 for fixing multiple CVEs
- (1) CVE-2018-17189 (2) CVE-2018-17199 (3) CVE-2019-0190
- (4) CVE-2019-0211 (5) CVE-2019-0215 (6) CVE-2019-0217
* Thu Jan 24 2019 Dweep Advani <dadvani@vmware.com> 2.4.34-2
- Fixed CVE-2018-11763
* Wed Aug 29 2018 Tapas Kundu <tkundu@vmware.com> 2.4.34-1
- Updated to version 2.4.34, fix CVE-2018-1333
* Mon Oct 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.28-1
- Updated to version 2.4.28
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.27-3
- Remove shadow from requires and use explicit tools for post actions
* Mon Aug 07 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-2
- Add shadow to requires for useradd/groupadd
* Mon Jul 24 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-1
- Updated to version 2.4.27 - Fixes CVE-2017-3167
* Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.4.25-3
- Provide preset file to deactivate service by default.
* Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-2
- Fixing httpd.pid file write issue
* Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-1
- Updated to version 2.4.25
* Tue Dec 27 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-8
- BuildRequires lua, Requires lua.
* Wed Dec 21 2016 Anish Swaminathan <anishs@vmware.com>  2.4.18-7
- Change config file properties for httpd.conf
* Thu Jul 28 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-6
- Removed packaging of debug files
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-5
- Added patch for CVE-2016-5387
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.18-4
- GA - Bump release of all rpms
* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.4.18-3
- Adding upgrade support in pre/post/un script.
* Mon Mar 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.18-2
- Fixing systemd service
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-1
- Updated to version 2.4.18
* Mon Nov 23 2015 Sharath George <sharathg@vmware.com> 2.4.12-4
- Add /etc/mime.types
* Tue Sep 29 2015 Xiaolin Li <xiaolinl@vmware.com> 2.4.12-3
- Move perl script to tools package.
* Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-2
- Added service file. Changed installation paths.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-1
- Initial build. First version
