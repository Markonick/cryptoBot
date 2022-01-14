import React, { useEffect, useState } from 'react';
import axios from "axios";
import { AboutCard } from '../about/AboutCard';
import { GetOrders } from '../../api/GetOrders';
import OrdersTable from './OrdersTable';
import { IOrder } from "../../customTypes";

export const Orders: React.FC = () => {
  const about = { miaIqVersion: 0, ceMarkNumber: 0 }
  // const orders = GetOrders();

  const [orders, setOrders] = useState<IOrder[]>([]);
  // const baseUrl = process.env.REACT_APP_BASE_URL;
  const baseUrl = 'http://localhost:8000';
  useEffect(() => {
    const fetchOrders = async () => {
      console.log('BEFORE FETCHING ORDERS')
      await axios.get<IOrder[]>(`${baseUrl}/orders`).then(response => {
        console.log(response?.data)
        setOrders(response?.data);
      });
    };
    fetchOrders();
  }, []);
  console.log(orders)
  return (
    <>
      <OrdersTable></OrdersTable>
      {/* {orders} */}
    </>
  );
};