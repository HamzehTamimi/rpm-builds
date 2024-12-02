#
# spec file for package gnome-software-snapd
#

%define _unpackaged_files_terminate_build 0
%define gs_plugin_api 21
%bcond_with profiling

Name:           gnome-software-plugin-snapd
Version:        47.1
Release:        0
Summary:        GNOME Software Store with snapd
License:        GPL-2.0-or-later
Group:          System/GUI/GNOME
URL:            https://wiki.gnome.org/Apps/Software
Source0:        gnome-software-%{version}.tar.xz


BuildRequires:  gtk-doc
BuildRequires:  meson >= 0.58.0
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(appstream) >= 0.14.0
BuildRequires:  pkgconfig(flatpak) >= 0.6.12
BuildRequires:  pkgconfig(fwupd) >= 1.0.3
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.32.0
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gsettings-desktop-schemas) >= 3.11.5
BuildRequires:  pkgconfig(gsettings-desktop-schemas) >= 3.18.0
BuildRequires:  pkgconfig(gspell-1)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(json-glib-1.0) >= 1.2.0
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libhandy-1) >= 1.2.0
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(malcontent-0) >= 0.3.0
BuildRequires:  pkgconfig(ostree-1)
BuildRequires:  pkgconfig(packagekit-glib2) >= 1.1.0
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(xmlb) >= 0.1.7
%if %{with profiling}
BuildRequires:  pkgconfig(sysprof-capture-4)
%endif
# Additional dependencies for snapd integration
Requires:       gnome-software >= 47.0
BuildRequires:  pkgconfig(snapd-glib-2)
BuildRequires:  itstool
Requires:       snapd

%description
This subpackage provides the snapd plugin used by
the GNOME software store.

%prep
%autosetup -n gnome-software-%{version}

%build
# only build the snapd plugin
%meson \
    -D tests=false \
    -D man=false \
    -D packagekit=false \
    -D packagekit_autoremove=false \
    -D polkit=false \
    -D eos_updater=false \
    -D fwupd=false \
    -D flatpak=false \
    -D malcontent=false \
    -D rpm_ostree=false \
    -D webapps=false \
    -D hardcoded_foss_webapps=false \
    -D hardcoded_proprietary_webapps=false \
    -D gudev=false \
    -D apt=false \
    -D snap=true \
    -D external_appstream=false \
    -D gtk_doc=false \
    -D hardcoded_curated=false \
    -D default_featured_apps=false \
    -D mogwai=false \
    -D sysprof=disabled \
    -D profile='' \
    -D soup2=false \
    -D sysprof=%{?with_profiling:enabled}%{!?with_profiling:disabled} \
    %{nil}
# XXX we could build just the plugins/snap/gs_plugin_snap target, but the plugin
# target is not tagged and we cannot selectively install just the snap plugin's
# binaries
%meson_build 

%install
# XXX install everything
# TODO install just the snap plugin
%meson_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir %{_libdir}/gnome-software
%{_datadir}/applications/gnome-software-local-file-snap.desktop
%{_datadir}/metainfo/org.gnome.Software.Plugin.Snap.metainfo.xml
%dir %{_libdir}/gnome-software/plugins-%{gs_plugin_api}
%{_libdir}/gnome-software/plugins-%{gs_plugin_api}/libgs_plugin_snap.so

%changelog
