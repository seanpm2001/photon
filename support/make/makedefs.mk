MKDIR=/bin/mkdir
RM=/bin/rm
RMDIR=/bin/rm -rf
CP=/bin/cp
MV=/bin/mv
TAR=/bin/tar
RPMBUILD=/usr/bin/rpmbuild
SED=/usr/bin/sed
SHASUM=/usr/bin/shasum
ARCH?=$(shell uname -m)

SRCROOT := $(realpath $(SRCROOT))
MAKEROOT := $(realpath $(MAKEROOT))

PHOTON_BUILD_TYPE?=chroot
PHOTON_STAGE?=$(SRCROOT)/stage
PHOTON_LOGS_DIR=$(PHOTON_STAGE)/LOGS
PHOTON_RPMS_DIR=$(PHOTON_STAGE)/RPMS
PHOTON_SRPMS_DIR=$(PHOTON_STAGE)/SRPMS
PHOTON_UPDATED_RPMS_DIR?=$(PHOTON_STAGE)/UPDATED_RPMS
PHOTON_SPECS_DIR?=$(SRCROOT)/SPECS
PHOTON_COMMON_DIR?=$(SRCROOT)/common
PHOTON_DATA_DIR?=$(PHOTON_COMMON_DIR)/data
PHOTON_SRCS_DIR=$(PHOTON_STAGE)/SOURCES
PHOTON_PUBLISH_RPMS_DIR=$(PHOTON_STAGE)/PUBLISHRPMS
PHOTON_PUBLISH_XRPMS_DIR=$(PHOTON_STAGE)/PUBLISHXRPMS
PHOTON_GENERATED_DATA_DIR=$(PHOTON_STAGE)/common/data

PHOTON_PKG_BUILDER_DIR=$(SRCROOT)/support/package-builder
PHOTON_PULL_PUBLISH_RPMS_DIR=$(SRCROOT)/support/pullpublishrpms
PHOTON_IMAGE_BUILDER_DIR=$(SRCROOT)/support/image-builder

PHOTON_INSTALLER_DIR=$(SRCROOT)/installer
PHOTON_INSTALLER=$(PHOTON_INSTALLER_DIR)/photonInstaller.py
PHOTON_SPECDEPS_DIR=$(SRCROOT)/support/package-builder
PHOTON_SPECDEPS=$(PHOTON_SPECDEPS_DIR)/SpecDeps.py
PHOTON_PACKAGE_BUILDER=$(PHOTON_PKG_BUILDER_DIR)/builder.py
PHOTON_GENERATE_OSS_FILES=$(PHOTON_PKG_BUILDER_DIR)/GenerateOSSFiles.py
ifdef PHOTON_PULLSOURCES_CONFIG
PHOTON_PULLSOURCES_CONFIG:=$(abspath $(PHOTON_PULLSOURCES_CONFIG))
else
PHOTON_PULLSOURCES_CONFIG?=https://packages.vmware.com/photon/photon_sources/1.0
endif
PHOTON_PULL_PUBLISH_RPMS=$(PHOTON_PULL_PUBLISH_RPMS_DIR)/pullpublishrpms.sh
PHOTON_PULL_PUBLISH_RPMS_CACHED=$(PHOTON_PULL_PUBLISH_RPMS_DIR)/pullpublishrpms-cached.sh
PHOTON_PUBLISH_RPMS_URL?=https://packages.vmware.com/photon/photon_publish_rpms
PHOTON_PUBLISH_X_RPMS_URL?=https://packages.vmware.com/photon/photon_publish_x_rpms
PHOTON_IMAGE_BUILDER=$(PHOTON_IMAGE_BUILDER_DIR)/imagebuilder.py
PHOTON_PKGINFO_FILE=$(PHOTON_STAGE)/pkg_info.json

PHOTON_CHROOT_CLEANER=$(PHOTON_PKG_BUILDER_DIR)/clean-up-chroot.py
PHOTON_RPMS_DIR_NOARCH=$(PHOTON_RPMS_DIR)/noarch
PHOTON_RPMS_DIR_ARCH=$(PHOTON_RPMS_DIR)/$(ARCH)
PHOTON_UPDATED_RPMS_DIR_NOARCH?=$(PHOTON_UPDATED_RPMS_DIR)/noarch
PHOTON_UPDATED_RPMS_DIR_ARCH?=$(PHOTON_UPDATED_RPMS_DIR)/$(ARCH)

PHOTON_CHROOT_PATH:=$(PHOTON_STAGE)/photonroot
PHOTON_FS_ROOT=/usr/src/photon
PHOTON_DIST_TAG?=.ph3
PHOTON_INPUT_RPMS_DIR?=$(SRCROOT)/inputRPMS

ifdef INPUT_PHOTON_BUILD_NUMBER
PHOTON_BUILD_NUMBER=$(INPUT_PHOTON_BUILD_NUMBER)
else
PHOTON_BUILD_NUMBER=$(shell git rev-parse --short HEAD)
endif
PHOTON_RELEASE_MAJOR_ID=3.0
PHOTON_RELEASE_MINOR_ID=
PHOTON_RELEASE_VERSION=$(PHOTON_RELEASE_MAJOR_ID)$(PHOTON_RELEASE_MINOR_ID)
PHOTON_DOCKER_PY_VER=2.3.0

PHOTON_PKG_BLACKLIST_FILE=""
PHOTON_REPO_TOOL?="createrepo"
PHOTON_REPO_TOOL_OPT="--update"

override PHOTON_DOCKER_IMAGE = "photon:3.0"
PH_BUILDER_TAG := "photon_builder:3.0"
ifndef PH3_DOCKER_IMG_URL
PH3_DOCKER_IMG_URL := "https://github.com/vmware/photon-docker-image/raw/$(shell uname -m)/3.0-20220715/docker/photon-rootfs-3.0-8e54ea3e7.tar.gz"
endif

ifndef BUILD_SRC_RPM
BUILD_SRC_RPM := 1
endif

ifndef BUILD_DBGINFO_RPM
BUILD_DBGINFO_RPM := 1
endif
