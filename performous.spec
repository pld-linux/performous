Summary:	Performous - The All-in-One Music Game
Summary(pl.UTF-8):	Performous - wiele gier muzycznych w jednej
Name:		performous
Version:	1.1
Release:	10
License:	GPL v2+
Group:		Applications/Sound
#Source0Download: https://github.com/performous/performous/releases
Source0:	https://github.com/performous/performous/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cf31d0973cd88b3cd626d312d6d3f5b2
Patch0:		%{name}-boost.patch
Patch1:		%{name}-pango1.44.patch
Patch2:		opencv-const.patch
URL:		http://performous.org/
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	SDL2-devel >= 2
BuildRequires:	boost-devel >= 1.36
BuildRequires:	cmake >= 2.8
# avformat avresample swscale
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	gettext-tools
BuildRequires:	glew-devel
BuildRequires:	glibmm-devel
BuildRequires:	help2man
BuildRequires:	libepoxy-devel >= 1.2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libsigc++-devel
BuildRequires:	libstdc++-devel >= 6:4.6
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxml++2-devel >= 2.6
BuildRequires:	opencv-devel
BuildRequires:	pango-devel >= 1:1.12
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	portmidi-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel
Suggests:	%{name}-tools = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An open-source karaoke, band and dancing game where one or more
players perform a song and the game scores their perform ances.
Supports songs in UltraStar, Frets on Fire and StepMania formats.
Microphones and instruments from SingStar, Guit ar Hero and Rock Band
as well as some dance pads are autodetected.

%description -l pl.UTF-8
Karaoke, gitara i taniec w jednej grze. Obsługuje utwory w formatach
UltraStar, Frets on Fire i StepManii. Mikrofony i kontrolery z gier
SingStar, Guitar Hero i Rock Band oraz maty do tańca są automatycznie
wykrywane.

%package tools
Summary:	Performous tools
Summary(pl.UTF-8):	Narzędzia do programu Performous
Group:		Applications/Sound

%description tools
Several utilities for converting data files for Performous.

%description tools -l pl.UTF-8
Zestaw narzędzi do konwersji danych dla programu Performous.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
	-DCMAKE_CXX_FLAGS_RELEASE="%{rpmcxxflags} -std=gnu++11" \
	-DCMAKE_DEBUG_FLAGS_RELEASE="%{debugcflags}" \
	-DMagick_LIBRARY="$(echo %{_libdir}/libMagickCore-*.so)" \
	-DMagick++_LIBRARY="$(echo %{_libdir}/libMagick++-*.so)"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p docs/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{zh,zh_CN}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt docs/{Authors,instruments}.txt
%attr(755,root,root) %{_bindir}/performous
%{_datadir}/games/%{name}
%{_mandir}/man6/performous.6*
%{_desktopdir}/performous.desktop
%{_pixmapsdir}/performous.svg

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gh_*_decrypt
%attr(755,root,root) %{_bindir}/itg_pck
%attr(755,root,root) %{_bindir}/ss_*
%{_mandir}/man1/gh_*_decrypt.1*
%{_mandir}/man1/ss_*.1*
