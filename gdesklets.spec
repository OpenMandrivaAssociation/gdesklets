%define name	gdesklets
%define version	0.36
%define release	%mkrel 0.beta.1
%define oname	gDesklets

Summary:	GNOME Desktop Applets
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.gdesklets.de//downloads/%oname-%{version}beta.tar.bz2
Source1:	%name-32.png
Source2:	%name-16.png
#Patch0:		%{oname}-0.34.1-no-mime-update.patch
License:	GPL
Group:		Graphical desktop/GNOME
URL:		http://www.gdesklets.de/
BuildRequires:	gnome-python-devel
BuildRequires:  pyorbit-devel  
BuildRequires:	pygtk2.0-devel > 2.4.0
BuildRequires:  librsvg2-devel 
BuildRequires:	libgtop2.0-devel >= 2.8.0
BuildRequires:	libxdmcp-devel
BuildRequires:  libxau-devel
BuildRequires:	gnome-python >= 2.0.0
BuildRequires:	libgnome2-devel > 2.6.0
BuildRequires:  desktop-file-utils, libgnomeui2-devel >= 2.2.0
BuildRequires:	librsvg-devel swig automake intltool
Requires:	gnome-python-gconf >= 2.6.0
Requires(Pre):	shared-mime-info
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:	gnome-python gnome-python-gconf gnome-python-gtkhtml2
Requires:	gnome-python-gnomevfs
Obsoletes:	gdesklets-starter-kit gdesklets-externalsensor
Provides:	gdesklets-externalsensor

%description
'gDesklets' provides an advanced architecture for desktop applets -
tiny displays sitting on your desktop in a symbiotic relationship of
eye candy and usefulness.

Populate your desktop with status meters, icon bars, weather sensors,
news tickers... whatever you can imagine! Virtually anything is
possible and maybe even available some day.

%prep
%setup -q -n %{oname}-%{version}beta

%build
%configure2_5x --disable-schemas-install
%make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

#remove mime related stuff
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/mime/application
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/mime/{globs,magic,XMLnamespaces,aliases,subclasses,mime.cache}
rm -f ${RPM_BUILD_ROOT}%{_datadir}/applications/mimeinfo.cache

#fix exec symlink for x86_64
rm -f ${RPM_BUILD_ROOT}%{_bindir}/%{name}
ln -s ${RPM_BUILD_ROOT}%{_libdir}/%{name} ${RPM_BUILD_ROOT}/%{_bindir}/%{name}
 

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

%post
%{update_menus}
%{update_desktop_database}

%postun
%{clean_menus}
%{clean_desktop_database}

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


