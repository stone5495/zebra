#coding=utf-8
from django.core.management import BaseCommand
from django.conf import settings

from common.apis.es import es, es_rest_call

warehouse_data = [
    ('7C01', '无锡市润达物流有限公司'),
    ('8803', '上海梅盛运贸有限公司宏达库'),
    ('1L01', '宝钢物流铁山路码头库'),
    ('0U01', '宁波华埠物流有限公司'),
    ('4301', '上海永空实业有限公司'),
    ('3701', '浙江萧然钢材物流中心有限公司'),
    ('0H01', '天天控股集团有限公司'),
    ('9C01', '宁波甬江印务实业有限公司'),
    ('1901', '小额站丰源库'),
    ('0U02', '宁波华埠物流有限公司'),
    ('1C01', '杭州天申物资有限公司'),
    ('9E01', '上海宝亭工贸有限公司'),
    ('1101', '上海益钢仓储有限公司'),
    ('4801', '上海瀛晟实业有限公司'),
    ('3C01', '宝山区盛桥金属加工厂'),
    ('6801', '上海宝钢高强钢加工配送有限公司'),
    ('4401', '上海阔道物流有限公司'),
    ('1601', '上海宝越钢材加工配送有限公司'),
    ('0C01', '上海月宝钢材配送有限公司'),
    ('2G01', '上海华冶钢材加工有限公司B区'),
    ('0108', '运输公司罗泾仓库'),
    ('9703', '上海宝钢物流有限公司工贸库'),
    ('4501', '小额站北钢库'),
    ('1A01', '南昌宝江钢材加工配送有限公司'),
    ('01S17', '宝钢运输公司首易库'),
    ('0102', '宝钢运输二号库'),
    ('0801', '上海华际储运贸易有限公司'),
    ('5303', '上海贯桑工贸有限公司二号库'),
    ('5501', '小额站铁山仓库'),
    ('9702', '宝钢物流三冠库'),
    ('0106', '宝钢运输六号库'),
    ('1301', '上海宝腾物流有限公司'),
    ('8902', '新开源2号库'),
    ('2Q01', '上海盛桥实业有限公司'),
    ('01S11', '宝钢运输公司泗塘库'),
    ('5L01', '上海西浜实业公司'),
    ('0120', '宝钢运输公司西浜库'),
    ('1801', '上海远利国际物流有限公司'),
    ('1902', '宝钢小额站广纪库'),
    ('3902', '上海兴晟钢材加工有限公司2号库'),
    ('0107', '宝钢运输公司三号库-E3'),
    ('8B01', '上海仲鼎钢铁有限公司'),
    ('3902', '上海兴晟钢材加工有限公司1号库'),
    ('3301', '上海开元储运有限公司'),
    ('2F01', '上海铜灿联运有限公司'),
    ('0401', '上海劲申仓储有限公司'),
    ('0101', '上海宝钢运输有限公司'),
    ('9704', '宝钢物流8号库'),
    ('8901', '上海新开源物流有限公司'),
    ('5B01', '运输公司宝富库'),
    ('2H01', '上海泰普科贸有限公司'),
    ('5301', '上海贯桑工贸有限公司'),
    ('0125', '宝钢运输公司宝杨东仓库'),
    ('0119', '运输公司顺众仓库'),
    ('0E01', '江阴闽海仓储有限公司'),
    ('8811', '上海梅盛运贸有限公司梅林库'),
    ('8805', '梅盛开平库'),
    ('8801', '梅盛梅盛麦金源库'),
    ('8804', '上海梅盛运贸有限公司'),
    ('8810', '梅盛开平库'),
    ('8802', '上海梅盛运贸有限公司鑫源库'),
    ('9301', '南京文腾金属制品有限公司'),
    ('8807', '上海梅盛运贸有限公司麦金源库'),
    ('8809', '上海梅盛运贸有限公司汽提库'),
    ('8812', '上海梅盛运贸有限公司宏达'),
    ('8808', '梅盛大胜关库'),
    ('0D01', '广州市宝兴物流有限公司'),
    ('2C01', '上海宝臣物流有限公司'),
    ('5901', '安徽宝钢钢材配送有限公司'),
    ('2901', '杭州余杭梁运金属制品有限公司'),
    ('6001', '沪冶二号库'),
    ('6B01', '上海万汇物流有限公司'),
    ('4H01', '上海申特型钢有限公司'),
    ('6901', '上海宝丰钢材加工有限公司'),
    ('9701', '宝钢物流宝杨库'),
    ('4B01', '上海宝钺物流有限公司'),
    ('01S12', '宝钢运输公司宝鼎库'),
    ('0123', '宝钢运输公司友金库'),
    ('4G01', '杭州华强实业有限公司'),
    ('8E01', '上海长建钢材加工有限公司'),
    ('0122', '宝钢运输公司乾晋库'),
    ('0810', '华际六号库'),
    ('7901', '上海宝钢不锈钢加工配送有限公司'),
    ('3401', '中国二十冶集团有限公司'),
    ('9401', '宝钢物流同济路库'),
    ('0K01', '上海宝钢内河装卸联营站'),
    ('0124', '宝钢运输何婷源库'),
    ('9001', '上海海外钢材剪切配送有限公司'),
    ('4F01', '上海嘉音金属材料加工有限公司'),
    ('0103', '宝钢运输公司三号库'),
    ('7101', '上海宝新钢材剪切厂'),
    ('2501', '上海晨娇储运有限公司'),
    ('0802', '上海华际储运公司二号库'),
    ('1R01', '江苏高兴达物流有限公司'),
    ('3902', '上海兴晟钢材加工有限公司4号库'),
    ('0118', '运输公司浦盈库'),
    ('5B01', '上海宝富钢管有限公司'),
    ('2Y01', '上海精锐捷时达钢材加工有限公司'),
    ('3902', '上海兴晟钢材加工有限公司3号库'),
    ('3H01', '上海宜峰库'),
    ('2V01', '上海盛桥实业有限公司石太库'),
    ('3U01', '上海首易金属加工有限公司'),
    ('7E01', '本钢济福库'),
    ('4W01', '上海交钢物流有限公司'),
    ('5701', '武汉市福鑫仓储有限公司'),
    ('3Y01', '湖南畅达物流有限公司'),
    ('4T01', '江苏国信五矿物流有限公司'),
    ('5T01', '上海宝山杨北纵剪厂'),
    ('2001', '中国诚通金属（集团）公司西北公司'),
    ('H101', '宁波宝井钢材加工配送有限公司'),
    ('L101', '大连玺达国际物流有限公司'),
    ('8Q01', '南京玉带金属包装材料有限公司'),
    ('4201', '重庆港九股份有限公司九龙坡集装箱码头分公司'),
    ('4R01', '重庆中交港口发展有限公司'),
    ('2101', '重庆国储物流有限公司'),
    ('6V01', '南京双锐金属材料有限公司'),
    ('5Q01', '宁波市北仑区霞浦金盛金属加工厂'),
    ('3601', '重庆市铁建物流有限公司'),
    ('6Y01', '江苏佰亿博特实业有限公司'),
    ('1Y01', '重庆豪龙物流有限公司佛耳岩库'),
    ('6S01', '杭州舜翔实业有限公司'),
    ('H901', '深圳妈湾仓库'),
    ('H401', '山东宝华耐磨钢有限公司'),
    ('H301', '广州花都京建物流有限公司'),
    ('9M02', '贝多九江中外运仓库'),
    ('0M02', '和贵东莞荣轩库'),
    ('H701', '青岛金世纪实业有限公司'),
    ('K601', '广州精进汽车钢材部件有限公司'),
    ('3K03', '新通豪3号库'),
    ('3K01', '上海新通豪国际物流1号库'),
    ('3K04', '上海新通豪国际物流9号库'),
    ('1302', '上海宝腾物流有限公司3号库'),
    ('6H01', '常州苏泽金属制品有限公司'),
    ('6U01', '莱芜市紫林物流有限公司'),
    ('9901', '上海砺鑫钢铁加工配送有限公司'),
    ('2U01', '上海聚嘉源车业有限公司'),
    ('4Q01', '成都国储物流有限公司'),
    ('4T01', '江苏国信五矿物流有限公司三号库'),
    ('6R02', '上海澳洋顺昌金属材料有限公司'),
    ('8A01', '武汉西马钢铁物流有限公司'),
    ('8S01', '马鞍山市三和仓储配送有限公司'),
    ('4V01', 'P91627'),
    ('9V01', '上海镔铁金属（富锦库）'),
    ('3R01', '宁波宝骏物流有限公司'),
    ('0J01', '上海荷婷源实业有限公司'),
    ('2401', '宝钢大连物流中心'),
    ('0901', '重庆豪龙物流有限公司成都分公司'),
    ('1303', '上海宝腾物流有限公司2号库'),
    ('2301', '上海海泰储运有限公司'),
    ('3K01', '上海新通豪国际物流6号库'),
    ('5702', '武汉鑫港库'),
    ('3G01', '上海增富实业有限公司'),
    ('7X01', '杭州通钢国际控股有限公司'),
    ('1201', '中储发展股份有限公司天津塘沽分公司'),
    ('9Q01', '浙江冠川金属制品有限公司'),
    ('5K01', '上海君博钢材加工有限公司'),
    ('9L01', '韶关市韶宝钢材加工有限公司'),
    ('9M01', '贝多九江中外运仓库'),
    ('9M01', '贝多珠海高栏港仓库'),
    ('9M01', '贝多金博仓库'),
    ('9M01', '贝多江门高宝隆仓库'),
    ('0M01', '和贵东莞荣轩库'),
    ('0M01', '和贵姬堂仓'),
    ('0M01', '和贵丰乐仓'),
    ('0M01', '和贵力源仓'),
    ('H701', '青岛宝骏钢铁有限公司'),
    ('0D01', '宝兴石化仓库（1-3期）'),
    ('9W01', '申江集团有限公司'),
    ('K501', '广州兴攀加工有限公司'),
    ('k701', '泉州华锦码头'),
    ('0108', '运输公司顺能仓库'),
    ('5D01', '烟台宝井钢材加工有限公司'),
    ('0301', '怡百库测试库'),
    ('4M01', '上海泗塘实业公司'),
    ('6Q01', '常州新宝钢材加工有限公司'),
    ('5R01', '济南宝钢钢材加工配送有限公司'),
    ('7W01', '诚通集团南方金属有限公司加工分公司'),
    ('7V01', '上海宝联五金储运有限公司联谊路库'),
    ('7Q01', '上海文兆钢材剪切有限公司'),
    ('7H01', '天津津路钢铁加工配送有限公司'),
    ('5E01', '烟台市平顺物流有限公司'),
    ('7T01', '银龙阪和（武汉）钢材加工有限公司'),
    ('9R01', '广州能钢东莞中堂仓'),
    ('7Y01', '马鞍山长运物流港有限公司'),
    ('0D01', '宝兴骏豪仓'),
    ('K301', '广州市南沙安华储运有限公司'),
    ('9M03', '贝多珠海高栏港仓库'),
    ('K901', '揭阳光大'),
    ('9801', '上海宝矍实业有限公司'),
    ('7701', '金博库'),
    ('5F01', '上海冶津金属加工配送有限公司'),
    ('4F01', '上海嘉音金属材料加工有限公司'),
    ('0R01', '上海海泰储运有限公司烟台库'),
    ('3S01', '上海晨娇轻型房屋营造有限公司'),
    ('5V01', '上海晨珅金属材料加工有限公司'),
    ('5M01', '广州宝井昌'),
    ('5Y01', '南京宝喜库'),
    ('0D01', '广州市宝兴物流有限公司'),
    ('7K01', '舞钢远洋物资有限公司'),
    ('7N01', '上海宝巍钢材加工有限公司'),
    ('H801', '智德物流南沙仓库'),
    ('H502', '广州番禺南沙货运实业有限公司'),
    ('9Y01', '广州市韶钢港务有限公司韶钢三围仓库'),
    ('0M05', '和贵力源仓'),
    ('K801', '佛山市顺德区坤翔钢材加工有限公司'),
    ('K701', '泉州华锦码头'),
    ('8805', '梅盛国信滨江库'),
    ('5704', '黄石西马物流有限公司'),
    ('0813', '上海华际储运码头库'),
    ('3H01', '上海宜峰金属制品有限公司'),
    ('3W01', '武汉钢铁重工集团冶金重工有限公司'),
    ('3B01', '上海行宝顺钢管有限公司'),
    ('5703', '武汉清山港口吊装有限公司'),
    ('7D01', '上海奕通钢铁加工配送有限公司'),
    ('5X01', '亘锦库'),
    ('1D01', '国家物资储备局天津八三八处'),
    ('2V01', '建发物资石太物流基地（建发石太库）'),
    ('7U01', '南极光钢铁（上海）有限公司'),
    ('7801', '重庆祥镕物流有限公司'),
    ('2N01', '上海丰蕴钢材加工有限公司'),
    ('8Z01', '上海臻融实业有限公司'),
    ('8H01', '上海新树金属制品有限公司'),
    ('6R01', '江苏澳洋顺昌股份有限公司'),
    ('6R03', '广东澳洋顺昌金属材料有限公司'),
    ('H503', '广州南沙港口开发有限公司'),
    ('K101', '泉州展志钢材有限公司'),
    ('0D01', '宝兴广裕码头库'),
    ('9M05', '贝多江门高宝隆仓库'),
    ('9N01', '重庆公路运输集团纳溪沟港务有限公司'),
    ('7L01', '山东北铭网络科技有限公司'),
    ('3Z01', '郑州华丰钢铁物流园有限公司'),
    ('4V01', '上海释辰金属制品有限公司'),
    ('1Q01', '中部金属材料交易有限公司'),
    ('0902', '重庆豪龙物流有限公司成都分公司2号库'),
    ('4N01', '上海海泰储运有限公司月川库'),
    ('6501', '烟台远盛钢管有限责任公司'),
    ('5Z01', '南京鑫岳科技实业有限公司'),
    ('6W01', '山东钢联物流有限公司'),
    ('5W01', '上海池南贸易有限公司'),
    ('6Z01', '苏州东鸿瑞包装科技有限公司'),
    ('6P01', '苏州捷玛库'),
    ('7S01', '上海今江实业有限公司'),
    ('8K01', '济南宝益钢材加工有限公司'),
    ('8H01', '苏州冠捷金属制品有限公司'),
    ('H501', '广州巿晖骏物流有限公司梅山仓'),
    ('H201', '马鞍山钢晨钢铁物流园'),
    ('9W01', '杭州申江新型材料科技有限公司'),
    ('H601', '浙江物产物流投资有限公司上海分公司（宝丰库）'),
    ('9M04', '贝多金博仓库'),
    ('0M03', '和贵姬堂仓'),
    ('0M04', '和贵丰乐仓'),
    ('0116', '运输公司泰普库'),
    ('K201', '广州市浩达物流有限公司'),
    ('C101', '江苏中宝钢材配送有限公司'),
    ('R601', '上海泰沪钢材配送有限公司'),
    ('0121', '宝钢运输公司S21库'),
    ('WP00765', '天津象屿立业物流有限公司'),
    ('3V01', '宁波中盟实业有限公司'),
    ('C401', '天津市润飞钢材加工有限公司'),
    ('D701', '宜兴市宜港装卸储运有限公司'),
    ('M201', '温州市盈方金属制品有限公司'),
    ('8N01', '南京宝兴金属加工有限公司'),
    ('M301', '顺德区财盛钢材有限公司'),
    ('R201', '无锡双盛库'),
    ('R501', '无锡群盈仓储有限公司'),
    ('R701', '浙江华彩薄板仓库'),
    ('WP00586', '上海益钢仓储有限公司'),
    ('C301', '普耀库'),
    ('6M01', '宁波市镇海宝琳钢材有限公司'),
    ('6N01', '无锡市国茂金属制品有限公司'),
    ('R301', '上海聚方实业有限公司'),
    ('0119', '宝钢运输宝动2号库'),
    ('M401', '佛山市高明基业冷轧钢板有限公司'),
    ('D401', '宁波新广兴国际贸易有限公司'),
    ('D501', '中远物流黄岛钢材仓储中心'),
    ('C701', '无锡群益仓储有限公司'),
    ('R801', '上海祺啦钢材剪切加工有限公司'),
    ('D901', '无锡市中宝储运有限责任公司'),
    ('D801', '无锡市新新华储运有限公司'),
    ('WP00774', '上海象屿钢铁供应链有限公司'),
    ('M901', '南京方正金属材料有限公司'),
    ('5G01', '上海宝动实业有限公司二号库'),
    ('4Y01', '黄石顺鸿物流有限公司'),
    ('0M01', '广州市和贵物流有限公司'),
    ('C501', '天津润方库'),
]

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        index = 'excel'
        t = 'warehouse'

        try:
            es_rest_call('/%s/%s'%(index,t), 'DELETE')
        except:
            pass
        
        for code, name in warehouse_data:
            es.index('excel', 'warehouse', {
                'code': code,
                'name': name
            })

        print 'warehouse已建'

