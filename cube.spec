#
# Conditional build:
%bcond_with	cheaters	# unlimited energy and ammo
#
Summary:	Cube FPS game
Summary(pl):	Gra FPS Cube
Name:		cube
Version:	2004_05_22
Release:	0.7
License:	ZLIB
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/cube/%{name}_%{version}.tar.gz
# Source0-md5:	a0ae899d9af6ab65970d81bf3ccd94ee
Source1:	%{name}-wrapper.sh
Source2:	%{name}-client.desktop
Source3:	%{name}-server.desktop
Patch0:		%{name}-cheaters.patch
Patch1:		%{name}-fun.patch
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

%description -l pl
Cube jest open source'ow± gr± FPS zarówno dla wielu jak i jednego
gracza. Ten pakiet zawiera klienta.

%package server
Summary:	Cube FPS game server
Summary(pl):	Serwer gry FPS Cube
Group:		X11/Applications/Games

%description server
Cube is an open source multiplayer and singleplayer first person
shooter game. This package contains server application.

%description server -l pl
Cube jest open source'ow± gr± FPS zarówno dla wielu jak i jednego
gracza. Ten pakiet zawiera serwer.

%prep
%setup -q -n %{name}
chmod +w packages/{socksky,stecki}
cd source
unzip -o %{name}_%{version}_src.zip
%{?with_cheaters:%patch0 -p0}
%patch1 -p0


%build
cd source/enet
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
install source/src/cube_* $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/cube
install %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install -D $RPM_BUILD_ROOT%{_datadir}/%{name}/data/martin/ball2.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}-client.png
install -D $RPM_BUILD_ROOT%{_datadir}/%{name}/data/martin/ball2.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}-server.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* readme.html source/readme.txt source/src/CUBE_TODO.txt
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
