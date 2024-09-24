<template>
  <div>
    <div id="tituloPagina">
        <h1>Puntos de encuentro y Recorridos de evacuacion</h1>
    </div>

    <!-- Map -->
    <div id="mapid"  style="height:600px" ></div>
    <!-- Cards -->
    
    <div class="d-flex ">
    <!-- Dot cards -->
    <div class="card col-6" >
      <div class="card-header  border-dark mb-3 bg-info text-light text-center"> <h3> <i class="fas fa-map-marker-alt"></i> Puntos de encuentro</h3></div>
        <div 
          v-for="item in meetpoints.puntos_encuentro" 
          :key="item.id">
          {{ addMarker(item, mymap) }}
          <div class="card border-info mb-3">
            <div class="card-header bg-info text-light"> <h5> {{item.nombre}} </h5></div>
            <div class="card-body">
              <p class="card-text"> direccion: {{item.dirección}}</p>
              <p class="card-text"> telefono: {{item.telefono}}</p>
            </div>
          </div>
        </div>

      <!-- Paginartion -->
      <nav aria-label="Page navigation example">
        <ul class="pagination">
          <li class="page-item" v-on:click="getPreviousPagePuntos()"><a class="page-link" href="#">Anterior</a></li>
          <li class="page-item"   v-for="pagina in paginasDeMeetpoints" :key="pagina"  v-on:click="getDataPagina(pagina)"><a class="page-link" href="#" > {{pagina}}</a></li>
          <li class="page-item" v-on:click="getNextPagePuntos()"><a class="page-link" href="#">Siguiente</a></li>
        </ul>
      </nav>
      </div>

    <!-- Routes cards -->
    <div class="card col-6 " >
    <div class="card-header  border-dark mb-3 bg-success text-light text-center" > <h3> <i class="fas fa-route"></i> Rutas</h3></div>
      <div 
        v-for="ruta in evacuationRoutes.recorridos" 
        :key="ruta.id">
        {{ addRoute(ruta, mymap)}}
  

        <div class="card border-success mb-3 ">
          <div class="card-header bg-success text-light"> <h5> {{ruta.nombre}} </h5></div>
          <div class="card-body">
            <p class="card-text"> descripcion: {{ruta.descripcion}}</p>
            <p class="card-text"> cantidad de puntos: {{ruta.coordenadas.length}}</p>
          </div>
        </div>
      </div>
      <nav aria-label="Page navigation example">
        <ul class="pagination">
          <li class="page-item"  v-on:click="getPreviousPageRutas()"><a class="page-link" href="#">Anterior</a></li>
          <li class="page-item" v-for="pagina in paginasDeRutas" :key="pagina" v-on:click="getDataDeRutaPagina(pagina)"><a class="page-link" href="#" >{{pagina}}</a></li>
          <li class="page-item"  v-on:click="getNextPageRutas()"><a class="page-link" href="#">Siguiente</a></li>
        </ul>
      </nav>
    </div>
    </div>
    <!-- end cards -->

  </div>
</template>
<script>
  import leaflet from "leaflet";
  import axios from 'axios';
  const SERVER_URL = "https://admin-grupo13.proyecto2021.linti.unlp.edu.ar/api/";



  export default{
    name: "MeetPoint",
    data: () => ({
        meetpoints: [],
        evacuationRoutes:[],
        /* Paginado */
        puntosEncuentroPorPagina: "",
        puntosEncuentroTotal: "",
        puntosPaginaActual: 1,
        /* paginado rutas */
        rutasPorPagina: "",
        rutasTotal: "",
        rutasPaginaActual: 1,

        /*  */
        paginasDeMeetpoints: "",
        paginasDeRutas: "",
    }),
    methods: {
      async getMeetPoints(pagina) {
        axios.get(SERVER_URL+'/puntos-encuentro/?page=' + pagina)
              .then(response => {
              // JSON responses are automatically parsed.
              console.log(response.data);
                this.meetpoints = response.data;
                this.puntosEncuentroPorPagina = response.data.puntos_encuentro.length;
                this.puntosEncuentroTotal = response.data.total
                this.paginasDeMeetpoints =  (Math.ceil( this.puntosEncuentroTotal/ this.puntosEncuentroPorPagina))
              })
              .catch(e => {
                console.log(e)
              })
    },
    async getRoutes(pagina) {
        axios.get(SERVER_URL+'/recorridos-evacuacion/?page=' + pagina )
              .then(response => {
              // JSON responses are automatically parsed.
                this.evacuationRoutes = response.data;
                this.rutasPorPagina = response.data.recorridos.length;
                this.rutasTotal = response.data.total;
                this.paginasDeRutas = (Math.ceil( this.rutasTotal/ this.rutasPorPagina))
                console.log(this.rutasPorPagina)
              })
              .catch(e => {
                console.log(e)
              })
    },
    addMarker(meetpoints,mymap) {
      console.log(meetpoints.id)
      var marker = leaflet
        .marker([meetpoints.lat, meetpoints.long])
        .addTo(mymap);
      marker.bindPopup( 
          "<b>  "+ meetpoints.nombre + " </b>"
      );
    },
    addRoute(route, mymap){
        let coordenadasDicc =  route.coordenadas;
        let coordenadas = [];
        coordenadasDicc.forEach(dato => {
            let cordenadasElem = [];
            cordenadasElem.push(parseFloat(dato.lat));
            cordenadasElem.push(parseFloat(dato.long));
            coordenadas.push(cordenadasElem);
            });
            leaflet.polyline(coordenadas, {color: "red"}).addTo(mymap); 
    },

    totalPaginas(){
      return Math.ceil( this.puntosEncuentroTotal/ this.puntosEncuentroPorPagina)
    },

    totalPaginasRuta(){
      return Math.ceil( this.rutasTotal/ this.rutasPorPagina)
     
    },

    getDataPagina(nroPagina){
      this.puntosPaginaActual = nroPagina;
      this.meetpoints =this.getMeetPoints(nroPagina);
    },


    getDataDeRutaPagina(nropagina){
      this.rutasPaginaActual = nropagina;
      this.evacuationRoutes = this.getRoutes(nropagina);
    },
  

    getPreviousPagePuntos(){
      if (this.puntosPaginaActual > 1){
        this.puntosPaginaActual--;
      }
      this.getDataPagina(this.puntosPaginaActual);
    },

    getNextPagePuntos(){
      if (this.puntosPaginaActual < this.totalPaginas()){
        this.puntosPaginaActual++;
      }
      this.getDataPagina(this.puntosPaginaActual);
    },

    getPreviousPageRutas(){
      if (this.rutasPaginaActual > 1){
        this.rutasPaginaActual--;
      }
      this.getDataDeRutaPagina(this.rutasPaginaActual);
    },

    getNextPageRutas(){
      if (this.rutasPaginaActual < this.totalPaginasRuta()){
        this.rutasPaginaActual++;
      }
      this.getDataDeRutaPagina(this.rutasPaginaActual);
    },

  },
  created() {
    this.meetpoints = this.getMeetPoints(1);
    this.evacuationRoutes = this.getRoutes(1);


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
