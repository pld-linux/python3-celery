
# TODO:
#	- consider init script / systemd job (uid/gid celery 274 used to be used)
#	  NOTE: this must not be included and enabled by default in the default
#	  package! Real-life deployments will mostly be application-specific.

# Conditional build:
%bcond_with	doc		# Sphinx documentation (too much dependencies to be worth the trouble)
%bcond_with	tests		# run tests (broken)

%define 	module	celery
Summary:	Celery - Distributed Task Query
Summary(pl.UTF-8):	Celery - rozproszona kolejka zadań
Name:		python3-%{module}
Version:	5.0.5
Release:	1
License:	BSD-like
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/c/celery/%{module}-%{version}.tar.gz
# Source0-md5:	a8193028841349fbc7c88e3b67ce608c
Patch0:		pytz_dependency.patch
URL:		http://celeryproject.org/
%if %{with tests}
BuildRequires:	python3-billiard >= 3.6.3.0
BuildRequires:	python3-billiard < 4
BuildRequires:	python3-boto3 >= 1.9.178
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-click >= 7.0
BuildRequires:	python3-click < 8
BuildRequires:	python3-click-didyoumean >= 0.0.3
BuildRequires:	python3-click-plugins >= 1.1.1
BuildRequires:	python3-click-repl >= 0.1.6
BuildRequires:	python3-kombu >= 5.0.0
BuildRequires:	python3-kombu < 6
BuildRequires:	python3-moto >= 1.3.7
BuildRequires:	python3-pytest >= 6.0
BuildRequires:	python3-pytest-celery
BuildRequires:	python3-pytest-subtests
BuildRequires:	python3-pytest-timeout >= 1.4.2
BuildRequires:	python3-pytz >= 2016.7
BuildRequires:	python3-vine >= 5.0.0
BuildRequires:	python3-vine < 6
%endif
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-billiard
BuildRequires:	python3-kombu >= 5.0.0
BuildRequires:	python3-pytz >= 2016.7
BuildRequires:	python3-sphinx_celery >= 2.0.0
BuildRequires:	python3-sphinx_click >= 2.5.0
BuildRequires:	python3-sphinx_testing >= 0.7.2
BuildRequires:	sphinx-pdg-3 >= 3.0.0
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%description -l pl.UTF-8
Celery to asynchroniczna kolejka zadań oparta na rozproszonym
przekazywaniu komunikatów. Skupia się na działaniu w czasie
rzeczywistym, ale obsługuje też szeregowanie.

%package -n celery
Summary:	Celery - Distributed Task Query
Summary(pl.UTF-8):	Celery - rozproszona kolejka zadań
Group:		Development/Languages/Python
Requires:	python3-%{module} = %{version}

%description -n celery
Celery is an asynchronous task queue/job queue based on distributed
message passing. It is focused on real-time operation, but supports
scheduling as well.

%description -n celery -l pl.UTF-8
Celery to asynchroniczna kolejka zadań oparta na rozproszonym
przekazywaniu komunikatów. Skupia się na działaniu w czasie
rzeczywistym, ale obsługuje też szeregowanie.

%package apidocs
Summary:	API documentation for Celery
Summary(pl.UTF-8):	Dokumentacja API Celery
Group:		Documentation

%description apidocs
API documentation for Celery.

%description apidocs -l pl.UTF-8
Dokumentacja API Celery.

%prep
%setup -q -n %{module}-%{version}

%patch0 -p1

%build
%py3_build %{?with_tests:test}

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs %{__sed} -i '1s|^#!.*python\b|#!%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt Changelog.rst LICENSE README.rst TODO extra/{generic-init.d,supervisord,systemd}
%{py3_sitescriptdir}/celery
%{py3_sitescriptdir}/celery-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}

%files -n celery
%defattr(644,root,root,755)
# TODO: extra/{bash-completion,zsh-completion}
%attr(755,root,root) %{_bindir}/celery

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,django,getting-started,history,internals,reference,tutorials,userguide,*.html,*.js}
%endif
