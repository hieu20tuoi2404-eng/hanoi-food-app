import React from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Home from './pages/Home'
import DishDetail from './pages/DishDetail'
import CollectionView from './components/collection/CollectionView'
import Settings from './pages/Settings'
import MascotPicker from './components/widgets/MascotPicker'
import { useApp } from './context/AppContext'

function AppRoutes() {
  const loc = useLocation()
  const onPickerPage = loc.pathname === '/chon-con-giap'
  return (
    <>
      {!onPickerPage && <Navbar />}
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dish/:slug" element={<DishDetail />} />
          <Route path="/bo-suu-tap" element={<CollectionView />} />
          <Route path="/cai-dat" element={<Settings />} />
          <Route path="/chon-con-giap" element={<MascotPicker />} />
        </Routes>
      </main>
    </>
  )
}

export default function App() {
  const { mascotReady, mascotId, pickerSeen } = useApp()
  const loc = useLocation()

  // First launch: show the zodiac picker as an overlay (never unmount the app,
  // so Home + Hoi Mèo stay mounted and stable while the user picks a mascot).
  const showFirstLaunch = mascotReady && !mascotId && !pickerSeen && loc.pathname !== '/chon-con-giap'

  return (
    <>
      <div className="app">
        <AppRoutes />
      </div>
      {showFirstLaunch && <MascotPicker />}
    </>
  )
}