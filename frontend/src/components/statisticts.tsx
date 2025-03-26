"use client"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Bar, BarChart, XAxis, YAxis } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface StatisticsData {
  school_data: Record<string, number>
  job_data: Record<string, number>
}

interface StatisticsDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  data: StatisticsData | null
}

export function StatisticsDialog({ open, onOpenChange, data }: StatisticsDialogProps) {
  if (!data) return null

  // Transform data for charts
  const schoolChartData = Object.entries(data.school_data).map(([name, count]) => ({
    name,
    count,
  }))

  const jobChartData = Object.entries(data.job_data).map(([title, count]) => ({
    title,
    count,  
  }))

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[650px] p-0 border-0">
        <DialogHeader className="p-6 pb-2">
          <DialogTitle className="text-xl font-bold">Candidate Statistics</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="schools" className="w-full">
          <div className="px-6">
            <TabsList className="grid w-full grid-cols-2 bg-gray-100">
              <TabsTrigger value="schools" className="data-[state=active]:bg-white">
                Schools
              </TabsTrigger>
              <TabsTrigger value="jobs" className="data-[state=active]:bg-white">
                Job Titles
              </TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value="schools" className="mt-2 p-6 pt-2">
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-2 bg-gray-50 rounded-t-lg">
                <CardTitle>Most Common Schools</CardTitle>
                <CardDescription>Distribution of candidates by school</CardDescription>
              </CardHeader>
              <CardContent className="p-4">
                <div className="h-[300px] w-full">
                  {schoolChartData.length > 0 ? (
                    <ChartContainer
                      config={{
                        count: {
                          label: "Candidates",
                          color: "hsl(215, 70%, 60%)",
                        },
                      }}
                    >
                      <BarChart
                        data={schoolChartData}
                        layout="vertical"
                        margin={{ left: 100, right: 20, top: 10, bottom: 10 }}
                      >
                        <XAxis type="number" />
                        <YAxis type="category" dataKey="name" width={90} tickLine={false} axisLine={false} />
                        <ChartTooltip content={<ChartTooltipContent />} />
                        <Bar dataKey="count" fill="#4285F4" radius={4} />
                      </BarChart>
                    </ChartContainer>
                  ) : (
                    <div className="flex items-center justify-center h-full text-muted-foreground">
                      No school data available
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="jobs" className="mt-2 p-6 pt-2">
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-2 bg-gray-50 rounded-t-lg">
                <CardTitle>Most Common Job Titles</CardTitle>
                <CardDescription>Distribution of candidates by job title</CardDescription>
              </CardHeader>
              <CardContent className="p-4">
                <div className="h-[300px] w-full">
                  {jobChartData.length > 0 ? (
                    <ChartContainer
                      config={{
                        count: {
                          label: "Candidates",
                          color: "hsl(150, 60%, 50%)",
                        },
                      }}
                    >
                      <BarChart
                        data={jobChartData}
                        layout="vertical"
                        margin={{ left: 100, right: 20, top: 10, bottom: 10 }}
                      >
                        <XAxis type="number" />
                        <YAxis type="category" dataKey="title" width={90} tickLine={false} axisLine={false} />
                        <ChartTooltip content={<ChartTooltipContent />} />
                        <Bar dataKey="count" fill="#34A853" radius={4} />
                      </BarChart>
                    </ChartContainer>
                  ) : (
                    <div className="flex items-center justify-center h-full text-muted-foreground">
                      No job title data available
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}

