# TODO: SysV init script? (Fedora has some old one)
#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	systemd		# systemd
#
Summary:	Partial implementation of iSNS (RFC 4171)
Summary(pl.UTF-8):	Częściowa implementacja iSNS (RFC 4171)
Name:		open-isns
Version:	0.102
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/open-iscsi/open-isns/releases
Source0:	https://github.com/open-iscsi/open-isns/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	914f7654ff7398dd4dcf69885f2fc691
URL:		https://github.com/open-iscsi/open-isns
BuildRequires:	meson >= 0.54.0
BuildRequires:	ninja
BuildRequires:	openslp-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.011
Requires:	%{name}-libs = %{version}-%{release}
Requires:	systemd-units >= 1:250.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open-iSNS is a partial implementation of iSNS, according to RFC 4171.

%description -l pl.UTF-8
Open-iSNS to częściowa implementacja iSNS, zgodnie z RFC 4171.

%package libs
Summary:	Shared Open-iSNS library
Summary(pl.UTF-8):	Biblioteka współdzielona Open-iSNS
Group:		Libraries

%description libs
Shared Open-iSNS library.

%description libs -l pl.UTF-8
Biblioteka współdzielona Open-iSNS.

%package devel
Summary:	Header files for Open-iSNS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Open-iSNS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Open-iSNS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Open-iSNS.

%package static
Summary:	Static Open-iSNS library
Summary(pl.UTF-8):	Statyczna biblioteka Open-iSNS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Open-iSNS library.

%description static -l pl.UTF-8
Statyczna biblioteka Open-iSNS.

%prep
%setup -q

%build
%meson build \
	%{?with_systemd:-Dsystemddir=%{_systemd_util_dir}} \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post isnsd.service

%preun
%systemd_preun isnsd.service

%postun
%systemd_postun isnsd.service

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/isnsadm
%attr(755,root,root) %{_sbindir}/isnsd
%attr(755,root,root) %{_sbindir}/isnsdd
%dir %{_sysconfdir}/isns
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/isns/isnsadm.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/isns/isnsd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/isns/isnsdd.conf
%if %{with systemd}
%{systemdunitdir}/isnsd.service
%{systemdunitdir}/isnsd.socket
%endif
%dir /var/lib/isns
%{_mandir}/man5/isns_config.5*
%{_mandir}/man8/isnsadm.8*
%{_mandir}/man8/isnsd.8*
%{_mandir}/man8/isnsdd.8*

%files libs
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libisns.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libisns.so
%{_includedir}/libisns
%{_pkgconfigdir}/libisns.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libisns.a
%endif
