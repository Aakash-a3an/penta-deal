<html>

<head>
    <meta charset="utf-8">
    <title>Price Comparison</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <meta content="Free HTML Templates" name="keywords">
    <meta content="Free HTML Templates" name="description">

    <!-- Favicon -->
    

    <!-- Google Web Fonts -->
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">  

    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css" rel="stylesheet">

    <!-- Libraries Stylesheet -->
    <link href="lib/animate/animate.min.css" rel="stylesheet">
    <link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">

    <!-- Customized Bootstrap Stylesheet -->
    <link href="css/style.css" rel="stylesheet">
</head>

<body>
    <!-- Topbar Start -->
    

    <!-- Navbar End -->


    <!-- Carousel Start -->
   
    <!-- Carousel End -->


    <!-- Featured Start -->
   
    <!-- Featured End -->


    <!-- Categories Start -->
    
    <!-- Categories End -->
		 <form action="" method="get">
		 <div class="row">
		 		<div class="col-md-2">
				</div>
				<div class="col-md-8">
				<p>Price Comparison</p>
                    <div class="input-group">
                        <input type="text" name="searchdata" class="form-control" placeholder="Search for products" required>
                        <div class="input-group-append">
                            <span class="input-group-text bg-transparent text-primary">
                                <button type="submit" name="bt" value="1"><i class="fa fa-search"></i></button>
                            </span>
                        </div>
                    </div>
				</div>
			</div>
                </form>

    <!-- Products Start -->
	
    <div class="container-fluid pt-5 pb-3">
        <h2 class="section-title position-relative text-uppercase mx-xl-5 mb-4"><span class="bg-secondary pr-3">Products</span></h2>
        <div class="row px-xl-5">
		
		<?php
//Get web page data by using URL ie web page link
error_reporting(E_ALL & ~E_NOTICE);
if(isset($_GET['searchdata']))
{
//if user enter searchdata then only show this
//pass searchdata to below link as search
$search = $_GET['searchdata'];
$search = strtolower($search);
//space to plus replace
$search = str_replace(" ","+",$search);
  $web_page_data = file_get_contents("http://www.pricetree.com/search.aspx?q=".$search);
  //we need particular data from page not entire page. echo $web_page_data;

  $item_list = explode('<div class="items-wrap">', $web_page_data); //from entire page it will split based on word <div class="items-wrap">
  //$item_list is arrat so print_r
  //print_r($item_list);
  $i=1;
  if(sizeof($item_list)<2){
    echo '<p><b>No results, enter proper product name Ex: Moto G</b></p>';
    $i=5;
  }
//variable to check no data
$count = 4;
  //avoid array[0] and loop for 4 items-wrap items and print them
  for($i;$i<5;$i++){

    //echo $item_list[$i]; //this is array saperated based on split string <div class="items-wrap">
    //I want title and another information
    //it is printing on 4 items
    //for those items i want item image url and item link
    //from list item split based on href=" and then " because we want url between them

    $url_link1 = explode('href="',$item_list[$i]);
    $url_link2 = explode('"', $url_link1[1]); //$url_link1[0] will be before http=" data
    //echo $url_link2[0]."</br>"; //split by " and before that

    //now image link, same as above but split with data-original="

    $image_link1 = explode('data-original="',$item_list[$i]);
    $image_link2 = explode('"', $image_link1[1]); //$image_link1[0] will be before data-original=" data
    //echo $image_link2[0]."</br>"; //split by " and before that

    //I want title and only avaliable
    //getting title split between title=" and "
    $title1 = explode('title="', $item_list[$i]);
    $title2 = explode('"', $title1[1]);

    //get only avaliable items
    //split between avail-stores"> and </div>
    $avaliavle1 = explode('avail-stores">', $item_list[$i]);
    $avaliable = explode('</div>', $avaliavle1[1]);
    if(strcmp($avaliable[0],"Not available") == 0) {
      //means not avaliable
      $count = $count-1;
      continue;
      //goto next item in for loop
    }

    $item_title = $title2[0];
    if(strlen($item_title)<2){
      continue;
    }
    $item_link = $url_link2[0];
    $item_image_link = $image_link2[0];
    $item_id1 = explode("-", $item_link);
    $item_id = end($item_id1); //split with "-" and print last one after split that is id
    //show image and product title
    echo '';
	?>
	<div class="col-lg-3 col-md-4 col-sm-6 pb-1">
                <div class="product-item bg-light mb-4">
                    <div class="product-img position-relative overflow-hidden">
     <img class="img-fluid w-100" src="<?php echo $item_image_link; ?>" alt="">
     </div>
                    <div class="text-center py-4">
                        <a class="h6 text-decoration-none text-truncate" href=""><?php echo $item_title ?></a>
                        <div class="d-flex align-items-center justify-content-center mt-2">
                          
                        </div>
						
						
						
                       <!-- <div class="d-flex align-items-center justify-content-center mb-1">
                            <small class="fa fa-star text-primary mr-1"></small>
                            <small class="fa fa-star text-primary mr-1"></small>
                            <small class="fa fa-star text-primary mr-1"></small>
                            <small class="fa fa-star text-primary mr-1"></small>
                            <small class="fa fa-star text-primary mr-1"></small>
                            <small>(99)</small>
                        </div>-->
						<?php

    //echo ."</br>";
    //echo $item_link."</br>";
    //echo $item_image_link."</br>";
    //echo $item_id."</br>";

    //goto pricetree access api to get price list
    //price list will be accessable based on $item_id

    $request = "http://www.pricetree.com/dev/api.ashx?pricetreeId=".$item_id."&apikey=7770AD31-382F-4D32-8C36-3743C0271699";
    $response = file_get_contents($request);
    $results = json_decode($response, TRUE);
    //print_r($results);
    //echo "-------------------------";
    //echo $results['count'];
    //table need to be open before for each
    //3 parts image and 9 parts table in a web page width
    echo '
  
      <table class="w3-table w3-striped w3-bordered w3-card-4">
      <thead>
      <tr class="w3-blue">
        <th>Seller_Name</th>
        <th>Price</th>
        <th>Buy Here</th>
      </tr>
      </thead>
    ';
	$a1=array();
	$a2=array();
	  $r=0;
    foreach ($results['data'] as $itemdata) {
      $seller = $itemdata['Seller_Name'];
      $price = $itemdata['Best_Price'];
      $product_link = $itemdata['Uri'];
      //echo $seller.",".$price.",".$product_link."</br>";
	 $a1[$r]=$price;
	 $a2[$r]=array($seller,$price,$product_link);
	 $r++;
	  }
	 asort($a1);
	  foreach($a1 as $ak=>$av)
	  {
  echo '

      <tr>
        <td>'.$a2[$ak][0].'</td>
        <td>'.$a2[$ak][1].'</td>
        <td><a href="'.$a2[$ak][2].'" target="_blank">Buy</a></td>
      </tr>

      ';
	  
	  }
	
    //close table after for each
    echo '
      </table>
    
    ';

?>
                    </div>
                </div>
            </div>
   

			<?php
			  }
  if($count == 0){
    echo '<p><b>No Products avaliable, Enter Proper Product Ex: Moto G</b></p>';
  }
}
else {
  echo '<p>Use this to get Best Price from all Sites. <b>Search Product to Know Price from All Online Shops</b></p>';
}
			?>
           
       
        </div>
		
	
		
		
    </div>
	
    <!-- Products End -->


    <!-- Offer Start -->
   
    <!-- Offer End -->


    <!-- Products Start -->
    
    <!-- Products End -->


    <!-- Vendor Start -->
    
    <!-- Vendor End -->


    <!-- Footer Start -->
   
    <!-- Footer End -->


    <!-- Back to Top -->
    <a href="#" class="btn btn-primary back-to-top"><i class="fa fa-angle-double-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>
    <script src="lib/easing/easing.min.js"></script>
    <script src="lib/owlcarousel/owl.carousel.min.js"></script>

    <!-- Contact Javascript File -->
    <script src="mail/jqBootstrapValidation.min.js"></script>
    <script src="mail/contact.js"></script>

    <!-- Template Javascript -->
    <script src="js/main.js"></script>
</body>

</html>