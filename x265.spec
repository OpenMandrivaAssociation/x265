%define major 215
%define oldlibname %mklibname x265 209
%define libname %mklibname x265
%define devname %mklibname x265 -d
%define staticname %mklibname x265 -d -s

%ifarch %{ix86}
# Workaround for buildtime error
# relocation R_386_GOTOFF against external symbol stderr cannot be used when making a shared object
%global __cc %{_bindir}/gcc
%global __cxx %{_bindir}/g++
%endif

Name:		x265
Version:	4.1
Release:	1
Source0:	https://bitbucket.org/multicoreware/x265_git/downloads/x265_%{version}.tar.gz
# Sources at https://www.videolan.org/developers/x265.html
# Original sources and faster releases here: https://bitbucket.org/multicoreware/x265_git/downloads/
Summary:	An H.265/HEVC encoder
URL:		https://x265.org/
License:	GPLv2, commercial licensing available for a fee
Group:		System/Libraries
BuildRequires:	yasm
BuildRequires:	nasm
BuildRequires:	git-core
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(numa)
Requires: %{libname} = %{EVRD}

%description
x265 is an open-source project and free application library
for encoding video streams into the H.265/High Efficiency
Video Coding (HEVC) format.

%package -n %{libname}
Summary: The x265 H.265/HEVC encoding library
Group: System/Libraries
Obsoletes: %{oldlibname} < %{EVRD}

%description -n %{libname}
x265 is an open-source project and free application library
for encoding video streams into the H.265/High Efficiency
Video Coding (HEVC) format.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package -n %{staticname}
Summary: Static library for %{name}
Group: Development/C
Requires: %{devname} = %{EVRD}

%description -n %{staticname}
Static library for %{name}

%prep
%autosetup -p1 -n %{name}_%{version}

git init
git config user.name "OpenMandriva Builder"
git config user.email "build@openmandriva.org"
git add .
git commit -am "Fake a git repository so X265_LATEST_TAG gets set"
git tag %{version}

MAJOR=$(grep 'set(X265_BUILD' source/CMakeLists.txt |sed -e 's,.*X265_BUILD ,,;s,).*,,')
if [ "$MAJOR" != "%{major}" ]; then
	echo "Please update major to $MAJOR"
	exit 1
fi

%build
%ifarch %{armx} %{arm}
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
%endif
pushd source
%cmake \
%ifnarch %{ix86}
	-DHIGH_BIT_DEPTH:BOOL=ON \
%endif
	-G Ninja
popd

pushd source/build
ninja %{_smp_mflags}
popd

%install
pushd source/build
DESTDIR=%{buildroot} ninja install
popd

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files -n %{staticname}
%{_libdir}/*.a
