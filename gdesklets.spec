%define name	gdesklets
%define version	0.36.3
%define release	1

Summary:	GNOME Desktop Applets
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
URL:            http://gdesklets.de/
Source0:	http://gdesklets.de/files/%{name}-%{version}.tar.bz2
Source1:	%{name}-32.png
Source2:	%{name}-16.png
Patch1:		gdesklets-0.36.3-no-import-override.patch
Patch3:		gdesklets-0.36.3-.in-files.patch
License:	GPLv2+
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gnome-python-devel
BuildRequires:  pyorbit-devel  
BuildRequires:	pygtk2.0-devel > 2.4.0
BuildRequires:  librsvg2-devel 
BuildRequires:	libgtop2.0-devel >= 2.8.0
BuildRequires:	libxdmcp-devel
BuildRequires:  libxau-devel
BuildRequires:	libgnome2-devel > 2.6.0
BuildRequires:  desktop-file-utils
BuildRequires:	libgnomeui2-devel >= 2.2.0
BuildRequires:	librsvg-devel intltool
Requires(pre):	shared-mime-info
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:	gnome-python
Requires:	gnome-python-gconf >= 2.6.0
Requires:	gnome-python-gtkhtml2
Requires:	gnome-python-gnomevfs

%description
'gDesklets' provides an advanced architecture for desktop applets -
tiny displays sitting on your desktop in a symbiotic relationship of
eye candy and usefulness.

Populate your desktop with status meters, icon bars, weather sensors,
news tickers... whatever you can imagine! Virtually anything is
possible and maybe even available some day.

%prep
%setup -q
%patch1 -p0
%patch3 -p0

%build
# FIXME: temporary workaround to get intltool-merge working. Will get fixed with a new release (> 0.36.1) released with a newer intltool.
#intltoolize --force --copy
autoreconf -f -i
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="System;Monitor" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*		  
 
install -d %{buildroot}%{_liconsdir}
ln -s %{_datadir}/pixmaps/%{name}.png %{buildroot}%{_liconsdir}
install -D %{SOURCE1} %{buildroot}%{_iconsdir}/%{name}.png
install -D %{SOURCE2} %{buildroot}%{_miconsdir}/%{name}.png

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-%{name}-display.png
%{_mandir}/man1/%{name}.1*
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
