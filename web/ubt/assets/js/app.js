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
        console.error('趋势分析图无数据');
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
          data: ['拉取的配送单总数', '完成整个蜂鸟配送流程的配送单数', '有效配送单量', '完成配送流程百分比', '有效配送单百分比']
        },
        xAxis: [{
          type: 'category',
          data: data.key
        }],
        yAxis: [{
          type: 'value',
          name: '单数（单）'
        },{
          type: 'value',
          name: '百分比（%）'
        }],
        series: [{
          name: '拉取的配送单总数',
          type: 'bar',
          data: data.total
        },{
          name: '完成整个蜂鸟配送流程的配送单数',
          type: 'bar',
          data: data.complete
        },{
          name: '有效配送单量',
          type: 'bar',
          data: data.valid
        },{
          name: '完成配送流程百分比',
          type: 'line',
          yAxisIndex: 1,
          data: data.percent
        },{
          name: '有效配送单百分比',
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