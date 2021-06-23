const assert = require('assert');
const formatDate = require('../format_date');
const moment = require('moment');

describe('Test formatDate', () => {

  // Takes a `date` and asserts that moments and formatDate are equal.
  function assertDateEquals(date) {
    let dateString = moment(date).format('D/MMM/YYYY:HH:mm:ss ZZ');
    let dateStringNew = formatDate(date)
    assert.equal(dateString, dateStringNew);
  }

  it('moment and formatDate should be equal for known date', () => {        
    assertDateEquals(new Date('January 12, 1989 12:32:17 EST'));
  });

  it('moment and formatDate should be equal for known date 0 date', () => {        
    assertDateEquals(new Date(0));
  });

  it('moment and formatDate should be equal for 100K random dates', () => {
    let interactions = 100000;
    for (let i=0; i<interactions; i++) {
      assertDateEquals(new Date(Math.random()* new Date().getTime()));
    }
  });
});