<h1 align="left">SmartPulse Case Preview</h1>

###

<p align="left">This project contains smart pulse case services on docker environment.</p>

###

<p align="left">It contains totally 6 different services and which are;</p>

###

<p align="left">🔹 Modbus Simulator<br>🔹 Modbus Reader<br>🔹 RabbitMQ<br>🔹 RabbitMQ Consumer Service<br>🔹 Prometheus TimeSeries Database<br>🔹 Grafana</p>

###

<p align="left">☑️ Docker Environment</p>

###

<p align="left">Docker environment created by compose and includes single network bridge to communicate micro services each other.</p>

###

<p align="left">☑️ Modbus Simulator</p>

###

<p align="left">This service developed in Python 3.9.0 Environment and depends on pymodbus library. It generates 3 random numbers and stores these numbers in 3 holding registers in modbus. Simulates modbus slave server environment and changes the register values in every seconds and can be connectable from every modbus master TCP connector.</p>

###

<p align="left">☑️ Modbus Reader</p>

###

<p align="left">This server is used to retrieve data from modbus simulator and send it to the RabbitMQ exchanger.</p>

###

<p align="left">☑️ RabbitMQ</p>

###

<p align="left">RabbitMQ service configured as having 1 Queue and 1 Exchange. Exchange is used for the elasticity because if there is any data source or different queues data should be reached, it can easily changes for this configuration.</p>

###

<p align="left">☑️ RabbitMQ Consumer Service</p>

###

<p align="left">This microservice developed in Python 3.9.0 environment and dockerized in compose environment. This service retrieves data from rabbitMQ queue and act as a prometheus data source to send data to prometheus time series database.</p>

###

<p align="left">☑️ Prometheus</p>

###

<p align="left">This Prometheus service used as data storage service to store holding register values. It's configured to use consumer service as datasource.</p>

###

<p align="left">☑️ Grafana</p>

###

<p align="left">Grafana tool used to visualize register values in timeseries domain.</p>

###

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" height="40" alt="docker logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/prometheus/prometheus-original.svg" height="40" alt="prometheus logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/grafana/grafana-original.svg" height="40" alt="grafana logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/ubuntu/ubuntu-plain.svg" height="40" alt="ubuntu logo"  />
</div>

###