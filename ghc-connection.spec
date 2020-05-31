#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	connection
Summary:	Simple and easy network connections API
Name:		ghc-%{pkgname}
Version:	0.3.1
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/connection
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6a9647665c357cd33118339b777578eb
URL:		http://hackage.haskell.org/package/connection
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-basement
BuildRequires:	ghc-data-default-class
BuildRequires:	ghc-network >= 2.6.3
BuildRequires:	ghc-socks >= 0.6
BuildRequires:	ghc-tls >= 1.4
BuildRequires:	ghc-x509 >= 1.5
BuildRequires:	ghc-x509-store >= 1.5
BuildRequires:	ghc-x509-system >= 1.5
BuildRequires:	ghc-x509-validation >= 1.5
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-basement-prof
BuildRequires:	ghc-data-default-class-prof
BuildRequires:	ghc-network-prof >= 2.6.3
BuildRequires:	ghc-socks-prof >= 0.6
BuildRequires:	ghc-tls-prof >= 1.4
BuildRequires:	ghc-x509-prof >= 1.5
BuildRequires:	ghc-x509-store-prof >= 1.5
BuildRequires:	ghc-x509-system-prof >= 1.5
BuildRequires:	ghc-x509-validation-prof >= 1.5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-basement
Requires:	ghc-data-default-class
Requires:	ghc-network >= 2.6.3
Requires:	ghc-socks >= 0.6
Requires:	ghc-tls >= 1.4
Requires:	ghc-x509 >= 1.5
Requires:	ghc-x509-store >= 1.5
Requires:	ghc-x509-system >= 1.5
Requires:	ghc-x509-validation >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library provides a very simple api to create sockets to a
destination with the choice of SSL/TLS, and SOCKS.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-basement-prof
Requires:	ghc-data-default-class-prof
Requires:	ghc-network-prof >= 2.6.3
Requires:	ghc-socks-prof >= 0.6
Requires:	ghc-tls-prof >= 1.4
Requires:	ghc-x509-prof >= 1.5
Requires:	ghc-x509-store-prof >= 1.5
Requires:	ghc-x509-system-prof >= 1.5
Requires:	ghc-x509-validation-prof >= 1.5

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build %{?_smp_mflags}
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Connection
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Connection/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Connection/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/Connection/*.p_hi
%endif
