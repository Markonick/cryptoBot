import { useEffect, useState } from 'react'
import ApiCore from './utilities/Core'

const ONE_MINUTE = 1*1000
const apiKline = new ApiCore({
  getAll: true,
  url: 'klines',
});

function GetKlineData(params) {
  const [data, setData] = useState()
  
  useEffect(() => {
    getDataPoints()
    const interval = setInterval(async () => { 
      getDataPoints()
    }, ONE_MINUTE);
    return () => clearInterval(interval);
  }, [])
  
  function getDataPoints() {
    apiKline.getAll(params).then((res) => {
      console.log(res)
      if(res !== undefined) {
        setData(res)
      }
    })
  }

  function parseData(data) {
    return data.map((item) => {
      // Parse data information
      return item
    })
  }

  return data
};

export default GetKlineData;