import React, { useEffect, useState } from 'react';
import axios from "axios";
import { AboutCard } from '../about/AboutCard';
import { GetOrders } from '../../api/GetOrders';
import { OrdersTable } from './OrdersTable';
import { IOrder } from "../../customTypes";

interface Props {
  pageSize: number;
  pageNumber: number;
}

export const Orders: React.FC<Props> = (props:Props) => {
  // const orders = GetOrders();

  const [orders, setOrders] = useState<IOrder[]>([]);
  const {pageSize, pageNumber} = props;
  // const baseUrl = process.env.REACT_APP_BASE_URL;
  const baseUrl = 'http://localhost:8000';
  useEffect(() => {
    const fetchOrders = async () => {
      console.log('BEFORE FETCHING ORDERS')
      const params={pageNumber: pageNumber, pageSize: pageSize}
      await axios.get<IOrder[]>(`${baseUrl}/orders`, {params}).then(response => {
        console.log(response?.data)
        setOrders(response?.data);
      });
    };
    fetchOrders();
  }, []);
  console.log(orders)
  return (
    <>
      <OrdersTable orders={orders}></OrdersTable>
      {/* {orders} */}
    </>
  );
};