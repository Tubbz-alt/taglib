Name:       taglib	
Summary:    Audio Meta-Data Library
Version:    1.9.1
Release:    1
Group:      System/Libraries

License:    LGPL-2.0+ or MPL-1.1
URL:        http://taglib.github.com/
Source0:    %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: zlib-devel
%if %{with doc}
BuildRequires: doxygen
BuildRequires: graphviz
%endif

%description
TagLib is a library for reading and editing the meta-data of several
popular audio formats. Currently it supports both ID3v1 and ID3v2 for MP3
files, Ogg Vorbis comments and ID3 tags and Vorbis comments in FLAC, MPC,
Speex, WavPack, TrueAudio files, as well as APE Tags.

%package doc
Summary: API Documentation for %{name}
BuildArch: noarch
%description doc
This is API documentation generated from the TagLib source code.

%package devel
Summary: Development files for %{name} 
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
%if ! %{with doc}
Obsoletes: %{name}-doc
%endif
%description devel
Files needed when building software with taglib.


%prep
%setup -q -n taglib-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%if %{with doc}
make docs -C %{_target_platform}
%endif


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%if %{with doc}
rm -fr %{apidocdir} ; mkdir %{apidocdir}
cp -a %{_target_platform}/doc/html/ %{apidocdir}/
ln -s html/index.html %{apidocdir}
find %{apidocdir} -name '*.md5' | xargs rm -fv
%endif


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion taglib)" = "%{version}"
test "$(pkg-config --modversion taglib_c)" = "%{version}"
%if %{with tests}
make check -C %{_target_platform}
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS
%doc COPYING.LGPL COPYING.MPL
%{_libdir}/libtag.so.1*
%{_libdir}/libtag_c.so.0*

%files devel
%doc examples
%{_bindir}/taglib-config
%{_includedir}/taglib/
%{_libdir}/libtag.so
%{_libdir}/libtag_c.so
%{_libdir}/pkgconfig/taglib.pc
%{_libdir}/pkgconfig/taglib_c.pc

%if %{with doc}
%files doc
%doc %{apidocdir}/*
%endif
