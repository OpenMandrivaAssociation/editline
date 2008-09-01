%define pversion 1.12

%define lib_major	0
%define lib_name_devel	%mklibname -d editline
%define lib_name	%mklibname editline %lib_major

Summary:	Line editing library similar to readline
Name:		editline
Version:	%{pversion}
Release:	%mkrel 12
Epoch:		0
License:	BSD-style
Group:		System/Libraries
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-build.patch
BuildRequires:	libtermcap-devel
BuildRequires:  libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Line editing library similar to readline.

%package -n %{lib_name}
Summary: Shared libraries for %{name}
Group: System/Libraries
Provides: %{name} = %{epoch}:%{version}-%{release}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked to %{name}.

%package -n %{lib_name_devel}
Summary: Files for developing programs that use the %{name} library
Group: Development/C
Requires: %{lib_name} = %{epoch}:%{version}-%{release}
Provides: lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides: %{name}-devel = %{epoch}:%{version}-%{release}
Provides: %{lib_name}-devel = %{epoch}:%{version}-%{release}
Obsoletes: %{lib_name}-devel

%description -n %{lib_name_devel}
Line editing library similar to readline.

%prep
%setup -q
%patch0 -p1

%build
%make CC="gcc $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}
install -m 644 .libs/lib%{name}.a $RPM_BUILD_ROOT%{_libdir}
install -m 755 .libs/lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}
(cd $RPM_BUILD_ROOT%{_libdir}; \
ln -sf lib%{name}.so.0.0.0 lib%{name}.so; \
ln -sf lib%{name}.so.0.0.0 lib%{name}.so.0)
install -d -m 755 $RPM_BUILD_ROOT%{_includedir}
install -m 644 include_editline.h $RPM_BUILD_ROOT%{_includedir}/editline.h
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man3
install -m 644 %{name}.3 $RPM_BUILD_ROOT%{_mandir}//man3
chmod 644 MANIFEST README

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root)
%doc MANIFEST README
%{_includedir}/*.h
%{_mandir}/man*/*
%{_libdir}/lib*.a
%{_libdir}/lib*.so
