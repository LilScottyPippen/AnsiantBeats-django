//Add to cart
$(document).on('click', ".button-buy", function() {
   let _vm = $(this);
   let _beatId = $(this).closest('.item-beat').find(".beat-id").val();
   let _beatCover = $(this).closest('.item-beat').find(".beat-cover").val();
   let _beatTitle = $(this).closest('.item-beat').find(".beat-title").val();
   let _beatType = $(this).closest('.item-beat').find(".beat-type").val();
   let _beatTonal = $(this).closest('.item-beat').find(".beat-tonal").val();
   let _beatBpm = $(this).closest('.item-beat').find(".beat-bpm").val();
   let _beatPrice = $(this).closest('.item-beat').find(".beat-price").val();

   let _totalSum = $('.total_cart').val();
   console.log("BeatID: " + _beatId, "BeatTitle: " + _beatTitle, "BeatType: " + _beatType , "ProductPrice: " + _beatPrice);
   //Ajax
   $.ajax({
      url: '/add-to-cart',
      data: {
         'beat_id': _beatId,
         'cover': _beatCover,
         'title': _beatTitle,
         'type': _beatType,
         'tonal': _beatTonal,
         'bpm': _beatBpm,
         'price': _beatPrice,
         'totalSum': _totalSum
      },

      dataType: 'json',
      beforeSend: function(){
         _vm.attr('disabled', true);
      },
      success: function(){
         _vm.attr('disabled', false);
         location.reload();
      }
   });
   //End
});
//End

//Delete item
$(document).on('click', '.delete-item', function (){
   let _bId = $(this).attr('data-item');
   let _vm = $(this);
   console.log(_bId);
   //Ajax
   $.ajax({
      url: '/delete-from-cart',
      data: {
         'beat_id': _bId,
      },
      dataType: 'json',
      success: function(res){
         _vm.attr('disabled', false);
         location.reload();
         $('.cart-products-container').html(res.data);
      }
   });
   //End
});
//End