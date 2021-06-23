var MONTH_NAMES = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
];

// Pad a value with the `0` character until it's length is equal to
// `len` or if no length is given pad to len=2.
function pad(val, len) {
  val = String(val);
  len = len || 2;
  while (val.length < len) {
    val = '0' + val;
  }
  return val;
}

// Formats dates to a common log formats time in strftime format 
// `%d/%b/%Y:%H:%M:%S %z.` Eg. 8/Dec/2018:14:47:51 -0500
// See: https://en.wikipedia.org/wiki/Common_Log_Format
function formatDate(date) {
  var offset = date.getTimezoneOffset();
  var tzOffset = (offset > 0 ? '-' : '+') 
                + pad(Math.floor(Math.abs(offset) / 60) 
                       * 100 + Math.abs(offset) % 60, 4);
  
  return date.getDate() + '/' 
         + MONTH_NAMES[date.getMonth()]
         + '/' + date.getFullYear()
         + ':' + pad(date.getHours())
         + ':' + pad(date.getMinutes())
         + ':' + pad(date.getSeconds())
         + ' ' + tzOffset;
}

module.exports = formatDate;