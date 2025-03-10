# TODO:
#	- consider init script / systemd job (uid/gid celery 274 used to be used)
#	  NOTE: this must not be included and enabled by default in the default
#	  package! Real-life deployments will mostly be application-specific.

# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_without	tests		# unit tests

%define 	module	celery
Summary:	Celery - Distributed Task Query
Summary(pl.UTF-8):	Celery - rozproszona kolejka zadań
Name:		python3-%{module}
Version:	5.2.7
Release:	2
License:	BSD-like
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/c/celery/%{module}-%{version}.tar.gz
# Source0-md5:	d684a4f20069c3c4c2f79e17fec42c52
URL:		http://celeryproject.org/
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-setuptools >= 1:40.8.0
%if %{with tests}
BuildRequires:	python3-billiard >= 3.6.4.0
BuildRequires:	python3-billiard < 4
BuildRequires:	python3-boto3 >= 1.9.178
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-click >= 8.0.3
BuildRequires:	python3-click < 9
BuildRequires:	python3-click-didyoumean >= 0.0.3
BuildRequires:	python3-click-plugins >= 1.1.1
BuildRequires:	python3-click-repl >= 0.2.0
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-importlib_metadata >= 1.4.0
%endif
BuildRequires:	python3-kombu >= 5.2.3
BuildRequires:	python3-kombu < 6
BuildRequires:	python3-moto >= 2.2.6
BuildRequires:	python3-pymongo
BuildRequires:	python3-pytest >= 6.2
BuildRequires:	python3-pytest-celery
BuildRequires:	python3-pytest-subtests
BuildRequires:	python3-pytest-timeout >= 1.4.2
BuildRequires:	python3-pytz >= 2021.3
BuildRequires:	python3-vine >= 5.0.0
BuildRequires:	python3-vine < 6
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-billiard >= 3.6.4.0
BuildRequires:	python3-kombu >= 5.2.3
BuildRequires:	python3-pytz >= 2021.3
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

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=celery.contrib.pytest,pytest_subtests \
%{__python3} -m pytest t/unit
%endif

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

install -d $RPM_BUILD_ROOT{%{bash_compdir},%{zsh_compdir}}
cp -p extra/bash-completion/celery.bash $RPM_BUILD_ROOT%{bash_compdir}/celery
cp -p extra/zsh-completion/celery.zsh $RPM_BUILD_ROOT%{zsh_compdir}/_celery

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
%attr(755,root,root) %{_bindir}/celery
%{bash_compdir}/celery
%{zsh_compdir}/_celery

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,django,getting-started,history,internals,reference,tutorials,userguide,*.html,*.js}
%endif
