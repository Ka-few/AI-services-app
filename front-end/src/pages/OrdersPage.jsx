import React from 'react'
import OrderList from '../components/OrderList'

function OrdersPage() {
  return (
    <div>
      <h1 style={{ textAlign: "center" }}>Bull Orders</h1>
        <OrderList />
    </div>
  )
}

export default OrdersPage
