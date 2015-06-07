(function () {

    var STATIC = {};
    STATIC.chart_id = ['overview','crawl','upload'];
    STATIC.base_url = '/overview';
    STATIC.param_chart = 'json';

    function _init(){
      loadChart();
    }

    function _getQuery(obj){
      return $.extend({
      }, obj);
    }

    function _ajax(obj, cb, name){
      $.ajax({
        url: STATIC.base_url+"/"+name,
        method: 'post',
        data: _getQuery(obj),
        success: cb
      });
    }

    function __getChartRef(chart_name){
      if(chart_ref == null){
        chart_ref = echarts.init(document.getElementById(chart_name));
      }
      return chart_ref;
    }

    function _paintChart(data){
      if($.isEmptyObject(data)){
        console.error('���Ʒ���ͼ������');
        return;
      }

      [data.percent, data.percent2].forEach(function(arr){
        arr.forEach(function(value, index){
          arr[index] = parseFloat(value * 100).toFixed(2);
        });
      });

      var opt = {
        tooltip : {
          trigger: 'axis'
        },
        legend: {
          data: ['��ȡ�����͵�����', '������������������̵����͵���', '��Ч���͵���', '����������̰ٷֱ�', '��Ч���͵��ٷֱ�']
        },
        xAxis: [{
          type: 'category',
          data: data.key
        }],
        yAxis: [{
          type: 'value',
          name: '����������'
        },{
          type: 'value',
          name: '�ٷֱȣ�%��'
        }],
        series: [{
          name: '��ȡ�����͵�����',
          type: 'bar',
          data: data.total
        },{
          name: '������������������̵����͵���',
          type: 'bar',
          data: data.complete
        },{
          name: '��Ч���͵���',
          type: 'bar',
          data: data.valid
        },{
          name: '����������̰ٷֱ�',
          type: 'line',
          yAxisIndex: 1,
          data: data.percent
        },{
          name: '��Ч���͵��ٷֱ�',
          type: 'line',
          yAxisIndex: 1,
          data: data.percent2
        }]
      }
      __getChartRef().setOption(opt);
    }

    function loadChart(){
      __getChartRef().showLoading();
      _ajax({type: STATIC.param_chart}, _paintChart);
    }

    function loadTable(){
      STATIC.$table.datagrid({
        url: STATIC.base_url,
        queryParams: _getQuery({type: STATIC.param_table})
      });
    }

    function refreshTable(){
      STATIC.$table.datagrid('load', _getQuery({type: STATIC.param_table}));
    }

    function downloadTable(){
      _download('post', STATIC.base_url, _getQuery({type: 'download'}));
    }

    $(window).ready(_init);
 })();