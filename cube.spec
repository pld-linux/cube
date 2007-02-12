# TODO
# - still vulnreable: http://security.gentoo.org/glsa/glsa-200603-10.xml
#
# Conditional build:
%bcond_with	cheaters	# unlimited energy and ammo
#
Summary:	Cube FPS game
Summary(pl.UTF-8):	Gra FPS Cube
Name:		cube
Version:	2005_08_29
Release:	0.1
License:	ZLIB
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/cube/%{name}_%{version}_unix.tar.gz
# Source0-md5:	e77f3cf85292bf61100d2f8511a254cc
Source1:	http://dl.sourceforge.net/cube/%{name}_%{version}_src.zip
# Source1-md5:	e376c49ac209b095cb6d29490834d060
Source2:	%{name}-wrapper.sh
Source3:	%{name}-client.desktop
Source4:	%{name}-server.desktop
Patch0:		%{name}-cheaters.patch
URL:		http://www.cubeengine.com/
BuildRequires:	OpenGL-devel-base
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	unzip
ExclusiveArch:	%{ix86} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Cube is an open source multiplayer and singleplayer first person
shooter game. This package contains client application.

%description -l pl.UTF-8
Cube jest open source'ową grą FPS zarówno dla wielu jak i jednego
gracza. Ten pakiet zawiera klienta.

%package server
Summary:	Cube FPS game server
Summary(pl.UTF-8):	Serwer gry FPS Cube
Group:		X11/Applications/Games

%description server
Cube is an open source multiplayer and singleplayer first person
shooter game. This package contains server application.

%description server -l pl.UTF-8
Cube jest open source'ową grą FPS zarówno dla wielu jak i jednego
gracza. Ten pakiet zawiera serwer.

%prep
%setup -q -n %{name} -a1
cd cube_source
%{?with_cheaters:%patch0 -p0}

%build
cd cube_source/enet
rm -f configure missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
cd ../src
%{__make} \
	COPTFLAGS="%{rpmcflags}" \
	CXXOPTFLAGS="%{rpmcflags} -fsigned-char -L/usr/X11R6/%{_lib} -DHAS_SOCKLEN_T=1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_desktopdir}}

cp -fr {data,packages} $RPM_BUILD_ROOT%{_datadir}/%{name}
install *.cfg $RPM_BUILD_ROOT%{_datadir}/%{name}
install cube_source/src/cube_* $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/cube
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
install -D $RPM_BUILD_ROOT%{_datadir}/%{name}/data/martin/ball2.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}-client.png
install -D $RPM_BUILD_ROOT%{_datadir}/%{name}/data/martin/ball2.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}-server.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* readme.html cube_source/readme.txt cube_source/src/CUBE_TODO.txt
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/cube_server
%{_datadir}/%{name}
%{_desktopdir}/%{name}-client.desktop
%{_pixmapsdir}/%{name}-client.png

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cube_server
%{_desktopdir}/%{name}-server.desktop
%{_pixmapsdir}/%{name}-server.png
