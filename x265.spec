%define major 61
# Version number is from "hg tip"
%define rev 10627
%define libname %mklibname x265 %{major}
%define devname %mklibname x265 -d
%define staticname %mklibname x265 -d -s

Name: x265
Version: 0.0.1
%if %{rev}
Release: 0.%{rev}.1
# hg clone https://bitbucket.org/multicoreware/x265
Source0: %{name}-%{rev}.tar.xz
%else
Release: 2
Source0: %{name}-%{version}.tar.xz
%endif
Patch0:	x265-6941-cmake-fix-pkgconfig-path.patch
Patch1:	x265-pic.patch
Patch2:	x265-test-shared.patch
Summary: An H.265/HEVC encoder
URL: http://x265.org/
License: GPLv2, commercial licensing available for a fee
Group: System/Libraries
BuildRequires: yasm
BuildRequires: cmake
BuildRequires: ninja

%description
x265 is an open-source project and free application library
for encoding video streams into the H.265/High Efficiency
Video Coding (HEVC) format.

%package -n %{libname}
Summary: The x265 H.265/HEVC encoding library
Group: System/Libraries

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
%if %{rev}
%setup -qn %{name}-%{rev}
%else
%setup -q
%endif
%apply_patches

%build
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
