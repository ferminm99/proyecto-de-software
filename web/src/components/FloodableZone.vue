<template>
  <div>
    <div id="tituloPagina">
      <h1> Zonas Inundables</h1>
    </div>
    <!-- Map -->
    <div id="mapid" style="height:600px"></div>

     <!-- Floodable Zones cards -->
    <div class="card col-12 " >
    <div class="card-header  border-dark mb-3 bg-info text-light text-center"> <h3> <i class="fas fa-route"></i> Zonas Indundables</h3></div>
      <div
        v-for="item in zones.zonas" 
        :key="item.id"
        v-bind:id="item.id">
          {{ drawZone(item, mymap)}}
          <div class="card border-success mb-3 ">
            <div class="card-header bg-info text-light "> <h5> {{item.nombre}} </h5></div>
            <div class="card-body">
              <p class="card-text"> color: {{item.color}}</p>
              <p class="card-text"> cantidad de puntos: {{item.coordenadas.length}}</p>
            </div>
            <div class="card-footer text-light  text-right"> <button class=" text-center bg- text-info"><router-link :to="`/verInfoZona/${item.id}`"> <h5> Ver detalles <i class="fas fa-sign-in-alt"></i> </h5> </router-link> </button> </div>
          </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
const SERVER_URL = "https://admin-grupo13.proyecto2021.linti.unlp.edu.ar/api/";
import leaflet from "leaflet";


export default {
  name: 'FloodableZone',
  data: () => ({
        zones: [],
    }),
  methods: {
    async get() {
        axios.get(SERVER_URL+'/zonas-inundables/')
              .then(response => {
              // JSON responses are automatically parsed.
                this.zones = response.data;
              })
              .catch(e => {
                console.log(e)
              })
    },
    drawZone(item, mymap){
      let coordenadasDicc =  item.coordenadas;
      let coordenadas = [];
      coordenadasDicc.forEach(dato => {
          let cordenadasElem = [];
          cordenadasElem.push(parseFloat(dato.lat));
          cordenadasElem.push(parseFloat(dato.long));
          coordenadas.push(cordenadasElem);
        });
        var polygon = leaflet.polygon(coordenadas, {color: item.color}).addTo(mymap); 
        polygon.bindPopup(item.nombre);
      }
  },
  props: {
    msg: String
  },
  
  created() {
    this.zones = this.get()
  },
  mounted() {
    this.mymap = leaflet.map("mapid").setView([-34.92114, -57.95502], 13);
    leaflet
      .tileLayer(
        "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw",
        {
          attribution:
            'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
          maxZoom: 18,
          id: "mapbox/streets-v11",
          tileSize: 512,
          zoomOffset: -1,
          accessToken: "your.mapbox.access.token",
        }
      )
      .addTo(this.mymap);
  },

}

</script>