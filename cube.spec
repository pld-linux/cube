
# TODO: desktop file

%bcond_with	cheaters	# unlimited energy and ammo

Summary:	Cube FPS game
Summary(pl):	Gra FPS Cube
Name:		cube
Version:	2003_12_23
Release:	1
License:	ZLIB
Group:		Applications/Games
Source0:	http://dl.sourceforge.net/cube/%{name}_%{version}.zip
# Source0-md5:	22555b87ef16c403198a6f378c048c6f
Source1:	%{name}-wrapper.sh
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

%description -l pl
Cube jest open source'ow± gr± FPS zarówno dla wielu jak i jednego
gracza. Ten pakiet zawiera klienta.

%package server
Summary:	Cube FPS game server
Summary(pl):	Serwer gry FPS Cube
Group:		Applications/Games

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
unzip %{name}_%{version}_src.zip
%{?with_cheaters:%patch0 -p0}

%build
cd source/%{name}_%{version}_src/enet
rm -f configure missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
cd ../src
%{__make} \
	COPTFLAGS="%{rpmcflags}" \
	CXXOPTFLAGS="%{rpmcflags} -fsigned-char -L/usr/X11R6/lib"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}}

cp -fr {data,packages} $RPM_BUILD_ROOT%{_datadir}/%{name}
install *.cfg $RPM_BUILD_ROOT%{_datadir}/%{name}
install source/%{name}_%{version}_src/src/cube_* $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/cube

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* readme.html source/readme.txt source/%{name}_%{version}_src/src/CUBE_TODO.txt
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/cube_server
%{_datadir}/%{name}

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cube_server
