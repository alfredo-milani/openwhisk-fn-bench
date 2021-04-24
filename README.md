# Progetto contenente composizione di funzini utilizzate per testare il comportamento di Apache OpenWhisk

* Il file "requirements.txt" è stato generato con il seguente comando: `pip freeze > requirements.txt`.
Nota(https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt)

* Eventualmente è possibile installare le dipendenze, con il comando: `pip install -r /path/to/requirements.txt`.
Nota(https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a)
  
### Note
* Per invocare scripts all'interno di package, e.g. `image_processing/resize.py`, è necessario impostare una variabile
d'ambiente con il comando: `$ export PYTHONPATH="${PWD}/src"`

* Per creare una **composition action** è possibile utilizzare [openwhisk-composer](https://github.com/apache/openwhisk-composer)
    * **openwhisk-composer** è utilizzato principalmente per JavaScript
    * Installare (globalmente o localmente) `openwhisk-composer`:
        * Spostarsi nella directory desiderata: `$ cd src/image_processing/composition`
        * Installare `openwhisk-composer`: `$ npm install openwhisk-composer`
    * Crea un file composizione (vedi esempio in `openwhisk-composer/samples/demo.js`)
    * Deploy composition (con `openwhisk-composer` installato localmente è necessario utilizzare il tool `npx`, altrimenti è possibile ometterlo): 
      `$ npx compose demo.js > demo.json` e `$ npx deploy demo demo.json -w`
    * Run composition: `$ wsk action invoke demo -p password passw0rd`
    * Get result: `$ wsk activation result 09ca3c7f8b68489c8a3c7f8b68b89cdc`

* Per creare una **composition action** utilizzando il linguaggio Python, è possibile utilizzare [openwhisk-composer-python](https://github.com/apache/openwhisk-composer-python)
    * E' necessario avere Python3.6 installato sul sistema
    * Installare `openwhisk-composer-python`:
        * `$ git clone https://github.com/apache/openwhisk-composer-python.git`
        * `$ cd composer-python`
        * `$ pip3 install -e .`
    * Crea un file composizione (vedi esempio in `openwhisk-composer-python/samples/demo.py`)
    * Deploy, Run, Get composizione è simile al corrispettivo in JavaScript (vedi sopra)
    * Nota: alla data attuale (14/12/2020) openwhisk-composer-python manca di alcune funzionalità (e.g. comando "parallel")

* Per l'installazione di Pillow (Python library), è necessario utilizzare un'immagine docker al cui interno creare un virtualenv con le dipendenze richieste; i passi sono i seguenti:
    * l'immagine docker necessaria è: openwhisk/python3action:1.15.0
    * una volta istanziato il container è necessario installare le seguenti librerie per la build della libreria
        * `$ apk add jpeg-dev zlib-dev`
    * assicurarsi che nella ${PWD} ci sia il file `requirements.txt` contente le specifiche delle dipendenze necessarie, ed eseguire il seguente comando: `$ virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt`
        * **NOTA**: è necessario che i comandi per il building delle librerie e la creazione del virtualenv avvengano su file system docker; per questo motivo il comando contenuto nel sito openwhisk deve essere modificato come segue: `$ docker run --rm -v "${RAMDISK}:/home/tmp" openwhisk/python3action:1.15.0 bash -c "apk add jpeg-dev zlib-dev && cp /home/tmp/requirements.txt /home && cd /home && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt && cp -r virtualenv /home/tmp"`
    * fare il packaging zip dei files necessari per il deploy della funzine: `$ zip -r helloPython.zip virtualenv __main__.py` 
        * assicurarsi che il file python contenente la funzione principale (main()) sia chiamato `__main__.py`
    * creare una azione OpenWhisk: `$ wsk action create helloPython --kind python:3 helloPython.zip`
        * **NOTA**: se la action necessita di binari che devono essere presenti nell'immagine docker (come nel caso di Pillow, che necessita di binari installati nell'immagine), allora si dobrebbe creare una custom [docker image](https://github.com/apache/openwhisk/blob/master/docs/actions-docker.md) ed uploadarla su Docker Hub.
        * **NOTA**: è stato provato ad utilizzare `$ zip -r -y resize.zip virtualenv __main__.py helper.py`, con il flag `-y` per archiviare i symbolic links (e non copiare il file a cui esso punta) e caricare la action con il comando `wsk action create resize --kind python:3 resize.zip`, ma l'esecuzione della action risultava in un errore: "The action failed to generate or locate a binary. See logs for details.".
        Questo suggerisce che è necessaria la creazione di una custom docker image.
        * **WORKAROUND**:
            1. elimina la corrente immagine `openwhisk/python3action:1.15.0` creata da openwhisk, se ce n'è una
            2. crea un Dockerfile come quello in `${PROJ}/FaaS/OpenWhisk/FunctionsComposition/resize_function/docker/Dockerfile` (vedere [link](https://github.com/apache/openwhisk/blob/master/docs/actions-docker.md)), installando i componenti necessari (in questo caso `jpeg-dev` e `zlib-dev`)
            3. fare una build dell'immagine e taggarla nello stesso modo in cui fa openwhisk, quindi `openwhisk/python3action:1.15.0`
            4. utilizzare openwhisk in modo consueto
* Per utilizzare le **web action** vedere il [link](https://github.com/apache/openwhisk/blob/master/docs/webactions.md)
    * invio di files binari, codifica/decodifica base64, ...
    * links aggiuntivi:
        * https://developer.ibm.com/recipes/tutorials/creating-a-openwhisk-web-action/
        * https://www.raymondcamden.com/2017/06/09/uploading-files-to-an-openwhisk-action
* Per utilizzare le **actions** vedere il [link](https://github.com/apache/openwhisk/blob/master/docs/actions.md)