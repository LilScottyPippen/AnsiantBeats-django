document.querySelector('.beats').addEventListener('click', () => {
    document.querySelector('.beats-container').style.display = 'block';
    document.querySelector('.beats').style.color = '#4885ff';
    document.querySelector('.beats').style.filter = 'invert(52%) sepia(63%) saturate(3695%) hue-rotate(203deg) brightness(99%) contrast(104%)';
    document.querySelector('.history-container').style.display = 'none';
    document.querySelector('.history').style.color = '';
    document.querySelector('.history').style.filter = '';
    document.querySelector('.profile-container').style.display = 'none';
    document.querySelector('.profile').style.color = '';
    document.querySelector('.profile').style.filter = '';
    document.querySelector('.password-container').style.display = 'none';
    document.querySelector('.password').style.color = '';
    document.querySelector('.password').style.filter = '';
    document.querySelector('.contact-container').style.display = 'none';
    document.querySelector('.contact').style.color = '';
    document.querySelector('.contact').style.filter = '';
    document.querySelector('.policy-container').style.display = 'none';
    document.querySelector('.policy').style.color = '';
    document.querySelector('.policy').style.filter = '';
}); 

document.querySelector('.history').addEventListener('click', () => {
    document.querySelector('.beats-container').style.display = 'none';
    document.querySelector('.beats').style.color = '';
    document.querySelector('.beats').style.filter = '';
    document.querySelector('.history-container').style.display = 'block';
    document.querySelector('.history').style.color = '#4885ff';
    document.querySelector('.history').style.filter = 'invert(52%) sepia(63%) saturate(3695%) hue-rotate(203deg) brightness(99%) contrast(104%)';
    document.querySelector('.profile-container').style.display = 'none';
    document.querySelector('.profile').style.color = '';
    document.querySelector('.profile').style.filter = '';
    document.querySelector('.password-container').style.display = 'none';
    document.querySelector('.password').style.color = '';
    document.querySelector('.password').style.filter = '';
    document.querySelector('.contact-container').style.display = 'none';
    document.querySelector('.contact').style.color = '';
    document.querySelector('.contact').style.filter = '';
    document.querySelector('.policy-container').style.display = 'none';
    document.querySelector('.policy').style.color = '';
    document.querySelector('.policy').style.filter = '';
}); 

document.querySelector('.profile').addEventListener('click', () => {
    document.querySelector('.beats-container').style.display = 'none';
    document.querySelector('.beats').style.color = '';
    document.querySelector('.beats').style.filter = '';
    document.querySelector('.history-container').style.display = 'none';
    document.querySelector('.history').style.color = '';
    document.querySelector('.history').style.filter = '';
    document.querySelector('.profile-container').style.display = 'block';
    document.querySelector('.profile').style.color = '#4885ff';
    document.querySelector('.profile').style.filter = 'invert(52%) sepia(63%) saturate(3695%) hue-rotate(203deg) brightness(99%) contrast(104%)';
    document.querySelector('.password-container').style.display = 'none';
    document.querySelector('.password').style.color = '';
    document.querySelector('.password').style.filter = '';
    document.querySelector('.contact-container').style.display = 'none';
    document.querySelector('.contact').style.color = '';
    document.querySelector('.contact').style.filter = '';
    document.querySelector('.policy-container').style.display = 'none';
    document.querySelector('.policy').style.color = '';
    document.querySelector('.policy').style.filter = '';
}); 

document.querySelector('.password').addEventListener('click', () => {
    document.querySelector('.beats-container').style.display = 'none';
    document.querySelector('.beats').style.color = '';
    document.querySelector('.beats').style.filter = '';
    document.querySelector('.history-container').style.display = 'none';
    document.querySelector('.history').style.color = '';
    document.querySelector('.history').style.filter = '';
    document.querySelector('.profile-container').style.display = 'none';
    document.querySelector('.profile').style.color = '';
    document.querySelector('.profile').style.filter = '';
    document.querySelector('.password-container').style.display = 'block';
    document.querySelector('.password').style.color = '#4885ff';
    document.querySelector('.password').style.filter = 'invert(52%) sepia(63%) saturate(3695%) hue-rotate(203deg) brightness(99%) contrast(104%)';
    document.querySelector('.contact-container').style.display = 'none';
    document.querySelector('.contact').style.color = '';
    document.querySelector('.contact').style.filter = '';
    document.querySelector('.policy-container').style.display = 'none';
    document.querySelector('.policy').style.color = '';
    document.querySelector('.policy').style.filter = '';
}); 

document.querySelector('.contact').addEventListener('click', () => {
    document.querySelector('.beats-container').style.display = 'none';
    document.querySelector('.beats').style.color = '';
    document.querySelector('.beats').style.filter = '';
    document.querySelector('.history-container').style.display = 'none';
    document.querySelector('.history').style.color = '';
    document.querySelector('.history').style.filter = '';
    document.querySelector('.profile-container').style.display = 'none';
    document.querySelector('.profile').style.color = '';
    document.querySelector('.profile').style.filter = '';
    document.querySelector('.password-container').style.display = 'none';
    document.querySelector('.password').style.color = '';
    document.querySelector('.password').style.filter = '';
    document.querySelector('.contact-container').style.display = 'block';
    document.querySelector('.contact').style.color = '#4885ff';
    document.querySelector('.contact').style.filter = 'invert(52%) sepia(63%) saturate(3695%) hue-rotate(203deg) brightness(99%) contrast(104%)';
    document.querySelector('.policy-container').style.display = 'none';
    document.querySelector('.policy').style.color = '';
    document.querySelector('.policy').style.filter = '';
}); 

document.querySelector('.policy').addEventListener('click', () => {
    document.querySelector('.beats-container').style.display = 'none';
    document.querySelector('.beats').style.color = '';
    document.querySelector('.beats').style.filter = '';
    document.querySelector('.history-container').style.display = 'none';
    document.querySelector('.history').style.color = '';
    document.querySelector('.history').style.filter = '';
    document.querySelector('.profile-container').style.display = 'none';
    document.querySelector('.profile').style.color = '';
    document.querySelector('.profile').style.filter = '';
    document.querySelector('.password-container').style.display = 'none';
    document.querySelector('.password').style.color = '';
    document.querySelector('.password').style.filter = '';
    document.querySelector('.contact-container').style.display = 'none';
    document.querySelector('.contact').style.color = '';
    document.querySelector('.contact').style.filter = '';
    document.querySelector('.policy-container').style.display = 'block';
    document.querySelector('.policy').style.color = '#4885ff';
    document.querySelector('.policy').style.filter = 'invert(52%) sepia(63%) saturate(3695%) hue-rotate(203deg) brightness(99%) contrast(104%)';
}); 



$(function(){
    $('.switch-btn').click(function (e, changeState) {
      if (changeState === undefined) {
        $(this).toggleClass('switch-on');
      }
      if ($(this).hasClass('switch-on')) {
        $(this).trigger('on.switch');
      } else {
        $(this).trigger('off.switch');
      }
    });
  
    $('.switch-btn').on('on.switch', function(){
      console.log('Кнопка переключена в состояние on');
    });
  
    $('.switch-btn').on('off.switch', function(){
      console.log('Кнопка переключена в состояние off');
    });
  
    $('.switch-btn').each(function(){
      $(this).triggerHandler('click', false);
    });
  
  });