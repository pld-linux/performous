Summary:	Performous - The All-in-One Music Game
Summary(pl.UTF-8):	Performous - wiele gier muzycznych w jednej
Name:		performous
Version:	1.3.0
Release:	1
License:	GPL v2+
Group:		Applications/Sound
#Source0Download: https://github.com/performous/performous/releases
Source0:	https://github.com/performous/performous/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1579905ea88e09611e90b737e9417895
Source1:	compact_enc_det.tar.xz
# Source1-md5:	c4af58e784fe054b787254acf5c1af12
Patch0:		ced-no-forced-cxx11.patch
Patch1:		find-ced.patch
Patch2:		no-Werror.patch
URL:		http://performous.org/
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	SDL2-devel >= 2
BuildRequires:	aubio-devel
BuildRequires:	boost-devel >= 1.36
BuildRequires:	cmake >= 2.8
# avformat avresample swscale
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	gettext-tools
BuildRequires:	glew-devel
BuildRequires:	glibmm-devel
BuildRequires:	gmock-devel
BuildRequires:	help2man
BuildRequires:	libepoxy-devel >= 1.2
BuildRequires:	libfmt-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libsigc++-devel
BuildRequires:	libstdc++-devel >= 6:4.6
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxml++2-devel >= 2.6
BuildRequires:	nlohmann-json-devel >= 3.10.5
BuildRequires:	opencv-devel
BuildRequires:	pango-devel >= 1:1.12
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	portmidi-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel
Obsoletes:	%{name}-tools < 1.3.0
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

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd compact_enc_det
install -d build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF
%{__make} ced
cp -p lib/libced.a ../compact_enc_det
cd ../..

SRC=$(pwd)
install -d build/game
cd build
%cmake .. \
	-DCMAKE_INSTALL_MANDIR=%{_mandir}/man6 \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
	-DCMAKE_CXX_FLAGS_RELEASE="%{rpmcxxflags}" \
	-DCMAKE_DEBUG_FLAGS_RELEASE="%{debugcflags}" \
	-DMagick_LIBRARY="$(echo %{_libdir}/libMagickCore-*.so)" \
	-DMagick++_LIBRARY="$(echo %{_libdir}/libMagick++-*.so)" \
	-DSELF_BUILT_CED=NEVER \
	-DCed_INCLUDE_DIRS="$SRC/compact_enc_det" \
	-DCed_LIBRARIES="-L$SRC/compact_enc_det/compact_enc_det $SRC/compact_enc_det/compact_enc_det/libced.a"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{zh,zh_CN}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md docs/{Authors,instruments}.txt
%attr(755,root,root) %{_bindir}/performous
%{_datadir}/games/%{name}
%{_mandir}/man6/performous.6*
%{_desktopdir}/performous.desktop
%{_pixmapsdir}/performous.svg
