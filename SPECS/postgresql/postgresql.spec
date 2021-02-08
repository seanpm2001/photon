Summary:        PostgreSQL database engine
Name:           postgresql
Version:        13.1
Release:        1%{?dist}
License:        PostgreSQL
URL:            www.postgresql.org
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha1    postgresql=3760c704f4d195100a28a983c0bc5331076259ee

# Common libraries needed
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  krb5-devel
BuildRequires:  libedit-devel
BuildRequires:  libxml2-devel
BuildRequires:  linux-api-headers
BuildRequires:  openldap
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  tar
BuildRequires:  tzdata
BuildRequires:  zlib-devel
Requires:       krb5
Requires:       libedit
Requires:       libxml2
Requires:       openldap
Requires:       openssl
Requires:       readline
Requires:       tzdata
Requires:       zlib

Requires:   %{name}-libs = %{version}-%{release}

%description
PostgreSQL is an object-relational database management system.

%package libs
Summary:    Libraries for use with PostgreSQL
Group:      Applications/Databases

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package        devel
Summary:        Development files for postgresql.
Group:          Development/Libraries
Requires:       postgresql = %{version}-%{release}

%description    devel
The postgresql-devel package contains libraries and header files for
developing applications that use postgresql.

%prep
%setup -q

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

%configure \
    --enable-thread-safety \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-libedit-preferred \
    --with-readline \
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --docdir=%{_docdir}/postgresql

make %{?_smp_mflags}
cd contrib && make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
cd contrib && make install DESTDIR=%{buildroot}

# For postgresql 10+, commands are renamed
# Ref: https://wiki.postgresql.org/wiki/New_in_postgres_10
ln -sf pg_receivewal %{buildroot}%{_bindir}/pg_receivexlog
ln -sf pg_resetwal %{buildroot}%{_bindir}/pg_resetxlog
ln -sf  pg_waldump %{buildroot}%{_bindir}/pg_xlogdump
%{_fixperms} %{buildroot}/*

%check
sed -i '2219s/",/  ; EXIT_STATUS=$? ; sleep 5 ; exit $EXIT_STATUS",/g'  src/test/regress/pg_regress.c
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/initdb
%{_bindir}/oid2name
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_basebackup
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_receivewal
%{_bindir}/pg_receivexlog
%{_bindir}/pg_recvlogical
%{_bindir}/pg_resetwal
%{_bindir}/pg_resetxlog
%{_bindir}/pg_rewind
%{_bindir}/pg_standby
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_upgrade
%{_bindir}/pg_waldump
%{_bindir}/pg_xlogdump
%{_bindir}/pg_checksums
%{_bindir}/pg_verifybackup
%{_bindir}/pgbench
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/vacuumlo
%{_datadir}/postgresql/*
%{_libdir}/postgresql/*
%{_docdir}/postgresql/extension/*.example
%exclude %{_datadir}/postgresql/pg_service.conf.sample
%exclude %{_datadir}/postgresql/psqlrc.sample

%files libs
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/dropuser
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_isready
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_libdir}/libecpg*.so.*
%{_libdir}/libpgtypes*.so.*
%{_libdir}/libpq*.so.*
%{_datadir}/postgresql/pg_service.conf.sample
%{_datadir}/postgresql/psqlrc.sample

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libecpg*.so
%{_libdir}/libpgtypes*.so
%{_libdir}/libpq*.so
%{_libdir}/libpgcommon*.a
%{_libdir}/libpgfeutils.a
%{_libdir}/libpgport*.a
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%{_libdir}/libecpg_compat.a
%{_libdir}/libpgtypes.a

%changelog
*   Fri Feb 5 2021 Michael Paquier <mpaquier@vmware.com> 13.1-1
-   Fix and reorganize list of BuildRequires
-   Removal of custom patch for CVE-2016-5423 committed in upstream.
-   Upgraded to version 13.1
*   Wed Sep 30 2020 Dweep Advani <dadvani@vmware.com> 13.0-3
-   Prefer libedit over readline
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 13.0-2
-   openssl 1.1.1
*   Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 13.0-1
-   Automatic Version Bump
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 12.4-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 12.3-1
-   Automatic Version Bump
*   Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 11.5-1
-   Upgraded to version 11.5
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 10.5-1
-   Updated to version 10.5
*   Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.8-1
-   Updated to version 9.6.8 to fix CVE-2018-1058
*   Mon Feb 12 2018 Dheeraj Shetty <dheerajs@vmware.com> 9.6.7-1
-   Updated to version 9.6.7
*   Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.6-1
-   Updated to version 9.6.6
*   Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.5-1
-   Updated to version 9.6.5
*   Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> 9.6.4-1
-   Updated to version 9.6.4
*   Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> 9.6.3-3
-   add sleep 5 when initdb in make check for bug 1900371
*   Wed Jul 05 2017 Divya Thaluru <dthaluru@vmware.com> 9.6.3-2
-   Added postgresql-devel
*   Tue Jun 06 2017 Divya Thaluru <dthaluru@vmware.com> 9.6.3-1
-   Upgraded to 9.6.3
*   Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 9.6.2-1
-   Upgrade to 9.6.2 for Photon upgrade bump
*   Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.3-6
-   Applied CVE-2016-5423.patch
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 9.5.3-5
-   Required krb5-devel.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 9.5.3-4
-   Modified %check
*   Thu May 26 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.3-3
-   Add tzdata to buildrequires and requires.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.5.3-2
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 9.5.3-1
-   Updated to version 9.5.3
*   Wed Apr 13 2016 Michael Paquier <mpaquier@vmware.com> 9.5.2-1
-   Updated to version 9.5.2
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.1-1
-   Updated to version 9.5.1
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.0-1
-   Updated to version 9.5.0
*   Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 9.4.4-1
-   Update to version 9.4.4.
*   Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 9.4.1-2
-   Exclude /usr/lib/debug
*   Fri May 15 2015 Sharath George <sharathg@vmware.com> 9.4.1-1
-   Initial build. First version
