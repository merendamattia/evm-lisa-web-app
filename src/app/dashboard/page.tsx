"use client"

import Dashboard from "@/components/dashboard-03"
import {
    TooltipProvider
  } from "@/components/ui/tooltip"
export default function test(){

    return(
        <TooltipProvider>
            <Dashboard></Dashboard>
        </TooltipProvider>
    )

}
