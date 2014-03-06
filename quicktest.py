from twotest.quicktest import QuickDjangoTest

if __name__ == '__main__':
    QuickDjangoTest(
        apps=("drole",),
        installed_apps=(
        "drole",
        ),
    )
