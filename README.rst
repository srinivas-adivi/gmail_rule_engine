
===================
** Build package **
===================

** Build ``smm`` with source file **
-----------------------------------------

- Create Python Virtual Environment ::

   > cd <path_to_smart_mail_manager>
   > python3 -m venv pyenv

- Build package with source file ::
   
   > cd <path_to_smart_mail_manager>
   > source pyenv/bin/activate
   > python setup.py build sdist

** Build ``smr`` with source file **
-----------------------------------------

- Create Python Virtual Environment ::

   > cd <path_to_smart_mail_router>
   > python3 -m venv pyenv

- Build package with source file ::
   
   > cd <path_to_smart_mail_router>
   > source pyenv/bin/activate
   > python setup.py build sdist

** Setup ``gre`` with source file **
-----------------------------------------

- Create Python Virtual Environment ::

   > cd <path_to_gmail_rule_engine>
   > python3 -m venv pyenv

-  Install dependencies ::

   > pip install <path_to_smart_mail_router>/dist/mart-mail-router-0.1.0.tar.gz
   > pip install <path_to_smart_mail_manager>/dist/mart-mail-manager-0.1.0.tar.gz
   > pip install -r requirements.txt 

** Prerequesites **
-------------------

- Python 3.10.12
- setuptools 59.6.0
- credentials.json 

** Usage **
-----------

- Activate Python Virtual Environment ::

   > cd <path_to_gmail_rule_engine>
   > source pyenv/bin/activate

- To store email in SQLite ::

   > python store_emails.py

- To process conditions and action on emails as mentioned in rules.json ::

   > python process_emails.py


** Reference **
---------------

- Create cloud project: https://developers.google.com/workspace/guides/create-project
- Configure Oauth:  https://developers.google.com/workspace/guides/configure-oauth-consent
- Create credentials: Access https://developers.google.com/workspace/guides/create-credentials
