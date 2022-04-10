# SFU CMPT 756 Term Project 

This is the term project repo for the team cloud_sprint from course CMPT 756 (Spring 2022)

### 1. Instantiate the template files

#### Fill in the required values in the template variable file

Copy the file `cluster/tpl-vars-blank.txt` to `cluster/tpl-vars.txt`
and fill in all the required values in `tpl-vars.txt`.  These include
things like your AWS keys, your GitHub signon, and other identifying
information.  See the comments in that file for details. Note that you
will need to have installed Gatling
(https://gatling.io/open-source/start-testing/) first, because you
will be entering its path in `tpl-vars.txt`.

#### Instantiate the templates

Once you have filled in all the details, run

~~~
$ make -f k8s-tpl.mak templates
~~~

This will check that all the programs you will need have been
installed and are in the search path.  If any program is missing,
install it before proceeding.

The script will then generate makefiles personalized to the data that
you entered in `clusters/tpl-vars.txt`.

**Note:** This is the *only* time you will call `k8s-tpl.mak`
directly. This creates all the non-templated files, such as
`k8s.mak`.  You will use the non-templated makefiles in all the
remaining steps.

### 2. Test CI locally
~~~
tools/shell.sh
/home/k8s# cd ci
/home/k8s# ./runci-local.sh v1
~~~

### 3. Ensure AWS DynamoDB is accessible/running

Regardless of where your cluster will run, it uses AWS DynamoDB
for its backend database. Check that you have the necessary tables
installed by running

~~~
$ aws dynamodb list-tables
~~~

The resulting output should include tables `User`, `Music` and `Playlist`.

### 4. Prerequisites
[Visual Studio Code (VSC)](https://code.visualstudio.com/)
[Git and GitHub Desktop](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
[Docker Desktop/Docker](https://docs.docker.com/get-docker/)
[aws-cli](https://github.com/aws/aws-cli)
[kubectl](https://kubernetes.io/docs/tasks/tools/)
[istioctl](https://github.com/istio/istio/tree/master/istioctl)


### 5. Commands for deployment and run in the cloud
1. start the container
~~~
tools/shell.sh
~~~
2. check if necessary tables installed
~~~
aws dynamodb list-tables
~~~
3. start aws cloud cluster
~~~
make -f eks.mak start
~~~
4. setup config files - kubeconfig & service mesh Istio
~~~
kubectl config use-context aws756
kubectl create ns c756ns
kubectl config set-context aws756 --namespace=c756ns
kubectl config use-context aws756
istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
kubectl label namespace c756ns istio-injection=enabled
~~~
5. build/deploy images with cri (short for container registry images)
~~~
make -f k8s.mak cri
make -f k8s.mak gw db s1 s2 s3
make -f k8s.mak loader
~~~
6. check if all the service are up
~~~
kubectl logs --selector app=cmpt756s1 --container cmpt756s1 --tail=-1
kubectl logs --selector app=cmpt756s2 --container cmpt756s2 --tail=-1
kubectl logs --selector app=cmpt756s3 --container cmpt756s3 --tail=-1
kubectl logs --selector app=cmpt756db --container cmpt756db --tail=-1
~~~
7. deploy all services
~~~
make -f k8s.mak provision
~~~

### 6. Grafana, Prometheus and Kiali
1. URLs
~~~
make -f k8s.mak grafana-url
make -f k8s.mak prometheus-url
make -f k8s.mak kiali-url
~~~
Sign on to Grafana with the following parameters:
User: admin
Password: prom-operator
After signon, you will see the Grafana home screen. Navigate to our dashboard by hovering on the “Dashboards” icon on the left. Select “Browse” from the menu. This will bring up a list of dashboards. Click on c756 transactions (it should be at or near the top of the list).
2. simulation
add up load progressively
~~~
./gatling-5-user.sh
./gatling-5-music.sh
./gatling-5-playlist.sh
~~~

~~~
./gatling-10-user.sh
./gatling-10-music.sh
./gatling-10-playlist.sh
~~~

~~~
./gatling-100-user.sh
./gatling-100-music.sh
./gatling-100-playlist.sh
~~~

~~~
./gatling-100-user.sh
./gatling-100-music.sh
./gatling-100-playlist.sh
~~~

3. stop gatling
~~~
tools/kill-gatling.sh
~~~

4. stup the cluster
~~~
make -f eks.mak stop
~~~

### 7. Structure of this repo

`ci`: continuous integration
`cluster`: to configure the cluster, should be treated with extra care such as not remove any lines from `.gitignore` file. 
`db`: the database service
`gatling`: for gatling simulation and tables
`loader`: for loading files into DynamoDB
`logs`: generated logs
`mcli`: CLI for the 3 microservices
`s1`: user service
`s2`: music service
`s3`: playlist service
`tools`: scripts for start the microsevices

```bash
.
├── dist (or build)
├── node_modules
├── bower_components (if using bower)
├── test
├── Gruntfile.js/gulpfile.js
├── README.md
├── package.json
├── bower.json (if using bower)
├── README.md
├── *.mak
├── *.gatling-N-SERVICE.sh
├── *.yaml
└── .gitignore
```
