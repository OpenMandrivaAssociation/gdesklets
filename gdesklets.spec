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
BuildRequires:  pkgconfig(librsvg-2.0) 
BuildRequires:	libgtop2.0-devel >= 2.8.0
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:  pkgconfig(xau)
BuildRequires:	pkgconfig(libgnome-2.0) > 2.6.0
BuildRequires:  desktop-file-utils
BuildRequires:	pkgconfig(libgnomeui-2.0) >= 2.2.0
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


%changelog
* Fri Mar 18 2011 Jani Välimaa <wally@mandriva.org> 0.36.3-1mdv2011.0
+ Revision: 646458
- new version 0.36.3
- drop old patches
- add a patch from gentoo to fix build/install
- fix url
- clean .spec a bit

* Mon Aug 16 2010 Emmanuel Andry <eandry@mandriva.org> 0.36.2-1mdv2011.0
+ Revision: 570542
- New version 0.36.2
- rediff p1

* Mon Nov 09 2009 Jérôme Brenier <incubusss@mandriva.org> 0.36.1-5mdv2010.1
+ Revision: 463767
- fix build (Patch2 added)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Mar 26 2009 Emmanuel Andry <eandry@mandriva.org> 0.36.1-3mdv2009.1
+ Revision: 361498
- add patch from archlinux to fix the -Could not import tiling module- error

* Tue Mar 24 2009 Emmanuel Andry <eandry@mandriva.org> 0.36.1-2mdv2009.1
+ Revision: 360902
- rebuild

* Sun Dec 07 2008 Funda Wang <fwang@mandriva.org> 0.36.1-1mdv2009.1
+ Revision: 311543
- new version 0.36.1

* Sat Aug 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.36-3mdv2009.0
+ Revision: 275322
- fix license
- use PO from opensuse
- use intltoolize

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sun Feb 24 2008 Emmanuel Andry <eandry@mandriva.org> 0.36-1mdv2008.1
+ Revision: 174473
- New version
- fix source
- BR reorganization
- disable x86_64 symlink workaround (should be fixed upstream)

* Tue Jan 08 2008 Emmanuel Andry <eandry@mandriva.org> 0.36-0.beta.2mdv2008.1
+ Revision: 146700
- fix wrong x86_64 symlink workaround

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 26 2007 Emmanuel Andry <eandry@mandriva.org> 0.36-0.beta.1mdv2008.1
+ Revision: 137823
- fix path for x86_64

* Tue Dec 18 2007 Emmanuel Andry <eandry@mandriva.org> 0.36-0.beta.0mdv2008.1
+ Revision: 132779
- New version

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 18 2007 Emmanuel Andry <eandry@mandriva.org> 0.35.4-4mdv2008.0
+ Revision: 89683
- make desktop file validation pass
- disable autotools since it generates errors with intltool-merge
- drop P0 and delete mime components manually (because of autotools deactivation)


* Sat Dec 09 2006 Emmanuel Andry <eandry@mandriva.org> 0.35.4-2mdv2007.0
+ Revision: 94384
- rebuild for python 2.5

* Tue Nov 07 2006 Emmanuel Andry <eandry@mandriva.org> 0.35.4-1mdv2007.1
+ Revision: 77055
- 0.35.4 (drop patch1)
- bunzip2 patches
- Import gdesklets

* Mon Sep 11 2006 Emmanuel Andry <eandry@mandriva.org> 0.35.3-4mdv2007.0
- rebuild

* Sat Aug 19 2006 Emmanuel Andry <eandry@mandriva.org> 0.35.3-3mdv2007.0
- patch from Nicolas L�cureuil to fix bug #24326

* Fri Aug 04 2006 Emmanuel Andry <eandry@mandriva.org> 0.35.3-2mdv2007.0
- fix mimetype
- works fine with default automake
- add buildrequires libgnomeui2_0-devel >= 2.2.0

* Sun Jul 23 2006 Emmanuel Andry <eandry@mandriva.org> 0.35.3-1mdv2007.0
- Reintroduced package with version 0.35.3 from fedora spec file
- Fixed URL for rpmbuildupdate
- %%mkrel
- xdg menu

