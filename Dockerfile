FROM python:3.4

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update
RUN apt-get install -y apt-utils openssh-server
RUN apt-get install -y sudo nano less vim tree mc
RUN apt-get install -y automake libtool libffi-dev curl git tmux gettext
# RUN apt-get install -y build-essential binutils-doc autoconf flex bison libjpeg-dev
# RUN apt-get install -y libfreetype6-dev zlib1g-dev libzmq3-dev libgdbm-dev libncurses5-dev

# postreg user and db in setup.sh

RUN apt-get install -y python3 python3-pip python-dev python3-dev python-pip virtualenvwrapper
RUN apt-get install -y libxml2-dev libxslt-dev

#
# RUN git clone https://github.com/taigaio/taiga-back.git taiga-back
# WORKDIR /taiga-back
# RUN git checkout stable

RUN adduser --disabled-password taiga && adduser taiga root && echo "%root ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers 
RUN mkdir /taiga-back
WORKDIR /taiga-back


RUN pip3 install virtualenvwrapper
RUN mkdir /home/taiga/.virtualenvs
RUN echo "export WORKON_HOME=/home/taiga/.virtualenvs; source /usr/local/bin/virtualenvwrapper.sh" >> /home/taiga/.bashrc
RUN echo "export WORKON_HOME=/home/taiga/.virtualenvs; source /usr/local/bin/virtualenvwrapper.sh" >> /root/.bashrc


COPY requirements.txt /taiga-back/requirements.txt
COPY migrate.sh /taiga-back/migrate.sh

RUN source /root/.bashrc && mkvirtualenv -p /usr/bin/python3.4 taiga
RUN source /root/.bashrc && workon taiga && pip install -r requirements.txt


RUN source /root/.bashrc && workon taiga && django-admin startproject taiga .
RUN chown -R taiga:taiga /home/taiga
RUN chown -R taiga:taiga /taiga-back
RUN chmod g+w /usr


USER taiga
RUN mkdir /home/taiga/logs
RUN mkdir -m 700 /home/taiga/.ssh
COPY ssh_key_igor_k_coretech.pub /home/taiga/.ssh/authorized_keys
RUN sudo chmod 600 /home/taiga/.ssh/authorized_keys
RUN sudo chown taiga:taiga /home/taiga/.ssh/authorized_keys

CMD sudo service ssh restart && \
    /home/taiga/.virtualenvs/taiga/bin/python manage.py runserver 0.0.0.0:8000
# CMD ["/home/taiga/.virtualenvs/taiga/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
