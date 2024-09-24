<template>
  <div>
    <div id="tituloPagina">
      <h1>Denuncias Confirmadas</h1>
    </div>
    <!--  <div v-for="item in complaints.complaints" :key="item.id">
      
     </div>
   Map -->
    <div class="row">
      <div class="col-md-8 col-12">
        <div id="mapid" style="height: 600px"></div>
      </div>
      <div class="col-md-4 col-12">
        <div class="tab-content bg-light" id="v-pills-tabContent">
          <div
            v-for="item in complaints.complaints"
            :key="item.id"
            class="tab-pane"
            v-bind:id="item.id"
            role="tabpanel"
            aria-labelledby="v-pills-"
          >
            {{ addMarker(item, mymap) }}
            <div class="row">
              <div class="col-12">
                <h4>{{ item.title }}</h4>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <small>{{ item.created_at }}</small>
              </div>
            </div>
            <div class="row py-2 border-bottom">
              <div class="col-md-2 col-12">
                <h6><strong> Dirección:</strong></h6>
              </div>
              <div class="col-md-10 col-12">
                <p>{{ item.address }}</p>
              </div>
            </div>
            <div class="row py-2 border-bottom">
              <div class="col-md-2 col-12">
                <h6><strong>Descripción:</strong></h6>
              </div>
              <div class="col-md-10 col-12">
                <p class="ml-2">{{ item.description }}</p>
              </div>
            </div>
            <div class="row py-2">
              <div class="col-md-2 col-12">
                <h6><strong>Estado:</strong></h6>
              </div>
              <div class="col-md-10 col-12">
                <p class="ml-2">{{ getState(item.id_state) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
//const SERVER_URL = "https://127.0.0.1:5000/api";
const SERVER_URL = "https://admin-grupo13.proyecto2021.linti.unlp.edu.ar/api";
import leaflet from "leaflet";

export default {
  name: "ShowComplaints",
  data: () => ({
    complaints: [],
  }),
  methods: {
    async get() {
      axios
        .get(SERVER_URL + "/denuncias/")
        .then((response) => {
          // JSON responses are automatically parsed.
          this.complaints = response.data;
          //console.log(response)
          //console.log(this.complaints)
        })
        .catch((e) => {
          console.log(e);
        });
    },
    addMarker(complaints, mymap) {
      var marker = leaflet
        .marker([complaints.latitude, complaints.length])
        .addTo(mymap);
      marker.bindPopup(
        '<div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical"><a class="nav-link" id="v-pills-' +
          complaints.id +
          '-tab" data-toggle="pill" href="#' +
          complaints.id +
          '" role="tab" aria-controls="v-pills-' +
          complaints.id +
          '" aria-selected="false">MAS INFO</a> </div>'
      );
    },
    getState(key) {
      let res = "Indefinida";
      switch (key) {
        case 2:
          res = "En curso";
          break;
        case 3:
          res = "Resuelta";
          break;
        case 4:
          res = "Cerrada";
          break;
        default:
          res;
          break;
      }
      return res;
    },
  },
  created() {
    this.get();
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
};
</script>