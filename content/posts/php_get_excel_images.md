---
Title:   PHPExcel读取EXCEL中的图片
Summary: PHPExcel是相当强大的 MS Office Excel 文档生成类库，当需要输出比较复杂格式数据的时候，PHPExcel 是个不错的选择。
Authors: Django Wong
Date:    2013-11-30
---

PHPExcel是相当强大的 MS Office Excel 文档生成类库，当需要输出比较复杂格式数据的时候，PHPExcel 是个不错的选择。  
经过认真研究API文档和查看官方文档，终于找到读取EXCEL中的图片，目前我只能读取excel 2003格式的。excel2007貌似还不支持。
其中主要使用的API为`PHPExcel_Worksheet`，`PHPExcel_Worksheet_BaseDrawing`，`PHPExcel_Worksheet_MemoryDrawing`。  

废话少说，直接上代码

	require_once './Classes/PHPExcel.php';
	$objPHPExcel = new PHPExcel();
	$objReader = PHPExcel_IOFactory::createReader('Excel5');  //加载2003的
	$objPHPExcel = $objReader->load("goods_list.xls");  //载入文件
	foreach ($objPHPExcel->getSheet(0)->getDrawingCollection() as $k => $drawing) {
			$codata = $drawing->getCoordinates(); //得到单元数据 比如G2单元
			$filename = $drawing->getIndexedFilename();  //文件名
			ob_start();
			call_user_func(
				$drawing->getRenderingFunction(),
				$drawing->getImageResource()
			);
			$imageContents = ob_get_contents();
			file_put_contents('pic/'.$codata.'_'.$filename.'.jpg',$imageContents); //把文件保存到本地
			ob_end_clean();
	}

