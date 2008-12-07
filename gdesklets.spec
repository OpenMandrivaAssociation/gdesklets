%define name	gdesklets
%define version	0.36.1
%define release	%mkrel 1

Summary:	GNOME Desktop Applets
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://gdesklets.de/files/%{name}-%{version}.tar.gz
Source1:	%name-32.png
Source2:	%name-16.png
Patch0:		destdir.patch
License:	GPLv2+
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-buildroot
URL:		http://www.gdesklets.de/
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
Requires:	gnome-python-gconf >= 2.6.0
Requires(Pre):	shared-mime-info
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:	gnome-python gnome-python-gconf gnome-python-gtkhtml2
Requires:	gnome-python-gnomevfs

%description
'gDesklets' provides an advanced architecture for desktop applets -
tiny displays sitting on your desktop in a symbiotic relationship of
eye candy and usefulness.

Populate your desktop with status meters, icon bars, weather sensors,
news tickers... whatever you can imagine! Virtually anything is
possible and maybe even available some day.

%prep
%setup -q -n gDesklets-%{version}
%patch0

%build
# FIXME: temporary workaround to get intltool-merge working. Will get fixed with a new release (> 0.36) released with a newer intltool.
intltoolize --force --copy
autoreconf -f -i
%configure2_5x --disable-schemas-install
%make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

#remove mime related stuff
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/mime/application
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/mime/{globs,magic,XMLnamespaces,aliases,subclasses,mime.cache}
#rm -f ${RPM_BUILD_ROOT}%{_datadir}/applications/mimeinfo.cache

perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="System;Monitor" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*		  
 
install -d %buildroot%_liconsdir
ln -s %_datadir/pixmaps/%name.png %buildroot%_liconsdir
install -D %SOURCE1 %buildroot%_iconsdir/%name.png
install -D %SOURCE2 %buildroot%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%{update_menus}
%{update_desktop_database}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%endif

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%_bindir/%name
%_libdir/%name
%_datadir/applications/%{name}.desktop
%_datadir/mime/packages/*
%_datadir/pixmaps/%{name}.png
%_datadir/icons/gnome/48x48/mimetypes/gnome-mime-application-x-%{name}-display.png
%_mandir/man1/%{name}.1*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png


