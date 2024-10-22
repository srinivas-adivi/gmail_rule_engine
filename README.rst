
===================
** Build package **
===================

** Build** ``smm`` ** with source file **
-----------------------------------------

- Create Python Virtual Environment

   > cd <path_to_smart_mail_manager>
   > python3 -m venv pyenv

- Build package with source file ::
   
   > cd <path_to_smart_mail_manager>
   > source pyenv/bin/activate
   > python setup.py build sdist

** Build** ``smr`` ** with source file **
-----------------------------------------

- Create Python Virtual Environment

   > cd <path_to_smart_mail_router>
   > python3 -m venv pyenv

- Build package with source file ::
   
   > cd <path_to_smart_mail_router>
   > source pyenv/bin/activate
   > python setup.py build sdist


- Create Python Virtual Environment

   > python3 -m venv pyenv
   > pip install <path_to_smart_mail_router>/dist/mart-mail-router-0.0.7.tar.gz
   > pip install <path_to_smart_mail_manager>/dist/mart-mail-manager-0.0.7.tar.gz
   > pip install -r requirements.txt 
