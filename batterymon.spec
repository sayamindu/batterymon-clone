%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

Summary: Battery level indicator for the GNOME panel
Name:    batterymon
Version: 1.2.4
Release: 1%{?dist}
License: LGPLv2+
Group:   Applications/System
URL:     http://code.google.com/p/batterymon
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: notify-python
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: python-devel
BuildRequires: python-distutils-extra
BuildArch: noarch

%description
This package contains a simple battery level indicator applet for GNOME. 
It can be useful for scenarios which do not have GNOME Power Manager installed 
for some reason.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
%{__python} setup.py install --root=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_datadir}/batterymon/icons/*
%{_bindir}/batterymon

%changelog
* Tue Jan 26 2010 Sayamindu Dasgupta <sayamindu@laptop.org>
- Initial packaging.
