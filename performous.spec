Summary:	Performous - The All-in-One Music Game
Summary(pl.UTF-8):	Performous - wiele gier muzycznych w jednej
Name:		performous
Version:	1.3.1
Release:	3
License:	GPL v2+
Group:		Applications/Sound
#Source0Download: https://github.com/performous/performous/releases
Source0:	https://github.com/performous/performous/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	02fd71009bc2ecece42f723aa4baca7c
Patch2:		no-Werror.patch
URL:		http://performous.org/
BuildRequires:	GLM-devel
BuildRequires:	SDL2-devel >= 2
BuildRequires:	aubio-devel >= 0.4.9
BuildRequires:	boost-devel >= 1.55
BuildRequires:	cairo-devel
BuildRequires:	cmake >= 3.15
BuildRequires:	compact_enc_det-devel
BuildRequires:	cpprestsdk-devel
# avformat swresample swscale
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	gettext-tools
BuildRequires:	glew-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	glibmm-devel >= 2.4
BuildRequires:	gmock-devel
BuildRequires:	help2man
BuildRequires:	libepoxy-devel >= 1.2
BuildRequires:	libicu-devel >= 60
BuildRequires:	libfmt-devel >= 9.0.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel >= 2
BuildRequires:	libsigc++-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxml++5-devel >= 5.0
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
%setup -q
%patch2 -p1

%build
%cmake -B build \
	-DCMAKE_INSTALL_MANDIR=%{_mandir}/man6 \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
	-DCMAKE_CXX_FLAGS_RELEASE="%{rpmcxxflags}" \
	-DCMAKE_DEBUG_FLAGS_RELEASE="%{debugcflags}" \
	-DSELF_BUILT_CED=NEVER

%{__make} -C build

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
%{_iconsdir}/hicolor/scalable/apps/performous.svg
