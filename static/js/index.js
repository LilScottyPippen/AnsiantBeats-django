const cards = document.querySelector(".container-last-beats");
const images = document.querySelectorAll(".last-beat-item-img, .button-to-playlist, .title-last-beats");
const backgrounds = document.querySelectorAll(".last-beat-item");
const range = 40;

// const calcValue = (a, b) => (((a * 100) / b) * (range / 100) -(range / 2)).toFixed(1);
const calcValue = (a, b) => (a/b*range-range/2).toFixed(1) // thanks @alice-mx

let timeout;

document.addEventListener('mousemove', ({x, y}) => {
  if (timeout) {
    window.cancelAnimationFrame(timeout);
  }
  	
  timeout = window.requestAnimationFrame(() => {
    const yValue = calcValue(y, window.innerHeight);
    const xValue = calcValue(x, window.innerWidth);

    cards.style.transform = `rotateX(${yValue}deg) rotateY(${xValue}deg)`;

    [].forEach.call(images, (image) => {
      image.style.transform = `translateX(${-xValue}px) translateY(${yValue}px)`;
    });

    [].forEach.call(backgrounds, (background) => {
      background.style.backgroundPosition = `${xValue*.45}px ${-yValue*.45}px`;
    })
	})
}, false);

// --------появление элементов-----------

function onEntry(entry) {
  entry.forEach(change => {
    if (change.isIntersecting) {
      change.target.classList.add('element-show');
    }
  });
}
let options = { threshold: [0.5] };
let observer = new IntersectionObserver(onEntry, options);
let elements = document.querySelectorAll('.element-animation');
for (let elm of elements) {
  observer.observe(elm);
}


function onEntry2(entry2) {
  entry2.forEach(change2 => {
    if (change2.isIntersecting) {
      change2.target.classList.add('element-show2');
    }
  });
}
let options2 = { threshold: [0.5] };
let observer2 = new IntersectionObserver(onEntry2, options2);
let elements2 = document.querySelectorAll('.element-animation2');
for (let elm2 of elements2) {
  observer2.observe(elm2);
}

function onEntry3(entry3) {
  entry3.forEach(change3 => {
    if (change3.isIntersecting) {
      change3.target.classList.add('element-show3');
    }
  });
}
let options3 = { threshold: [0.5] };
let observer3 = new IntersectionObserver(onEntry3, options3);
let elements3 = document.querySelectorAll('.element-animation3');
for (let elm3 of elements3) {
  observer3.observe(elm3);
}

// ------------------------------
// изменение цвета активного блока

var btn = document.getElementById("btn");
btn.addEventListener("click", function() {
  this.classList.add("active");
});


////для построения waveform

// Store the 3 buttons in some object
var buttons = {
  play: document.getElementById("btn-play"),
  pause: document.getElementById("btn-pause"),
  stop: document.getElementById("btn-stop")
};

// Create an instance of wave surfer with its configuration
var Spectrum = WaveSurfer.create({
  container: '#audio-spectrum',
  progressColor: "#03a9f4"
});

// Handle Play button
buttons.play.addEventListener("click", function () {
  Spectrum.play();

  // Enable/Disable respectively buttons
  buttons.stop.disabled = false;
  buttons.pause.disabled = false;
  buttons.play.disabled = true;
}, false);

// Handle Pause button
buttons.pause.addEventListener("click", function () {
  Spectrum.pause();

  // Enable/Disable respectively buttons
  buttons.pause.disabled = true;
  buttons.play.disabled = false;
}, false);


// Handle Stop button
buttons.stop.addEventListener("click", function () {
  Spectrum.stop();

  // Enable/Disable respectively buttons
  buttons.pause.disabled = true;
  buttons.play.disabled = false;
  buttons.stop.disabled = true;
}, false);


// Add a listener to enable the play button once it's ready
Spectrum.on('ready', function () {
  buttons.play.disabled = false;
});

// If you want a responsive mode (so when the user resizes the window)
// the spectrum will be still playable
window.addEventListener("resize", function () {
  // Get the current progress according to the cursor position
  var currentProgress = Spectrum.getCurrentTime() / Spectrum.getDuration();

  // Reset graph
  Spectrum.empty();
  Spectrum.drawBuffer();
  // Set original position
  Spectrum.seekTo(currentProgress);

  // Enable/Disable respectively buttons
  buttons.pause.disabled = true;
  buttons.play.disabled = false;
  buttons.stop.disabled = false;
}, false);

// Load the audio file from your domain !
Spectrum.load('/beats/yleti_remix.mp3');



//для ползунков 



