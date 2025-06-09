import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowDown } from "lucide-react";

const SignalDetail = ({ mfi, zcol }: { mfi?: string; zcol?: string }) => {
  const mfiColor =
    mfi === "++" ? "text-green-600" :
    mfi === "--" ? "text-yellow-600" :
    mfi === "-+" ? "text-red-600" :
    mfi === "+-" ? "text-gray-500" : "text-gray-400";

  return (
    <div className="text-xs mt-2">
      {mfi && <div className={`${mfiColor}`}>MFI: {mfi}</div>}
      {zcol && <div className="text-gray-500">Zone: {zcol}</div>}
    </div>
  );
};

const TrendBox = ({ label, trend, mfi, zcol }: { label: string; trend: string; mfi?: string; zcol?: string }) => {
  const color =
    trend === "Bullish"
      ? "bg-green-100 border-green-400"
      : trend === "Bearish"
      ? "bg-red-100 border-red-400"
      : "bg-gray-100 border-gray-300";

  return (
    <Card className={`${color} border text-center rounded-2xl shadow-md w-44`}>
      <CardContent className="p-4">
        <div className="font-bold text-lg mb-1">{label}</div>
        <div className="text-base font-medium">{trend}</div>
        <SignalDetail mfi={mfi} zcol={zcol} />
      </CardContent>
    </Card>
  );
};

const Arrow = () => (
  <div className="flex justify-center my-1">
    <ArrowDown className="h-5 w-5 text-gray-500" />
  </div>
);

const InstrumentBox = () => (
  <Card className="bg-white text-left rounded-2xl shadow-md w-60 mr-4 p-4">
    <div className="font-bold mb-1">Instrument</div>
    <div className="text-sm">SPX500</div>
  </Card>
);

const SourceBox = () => (
  <Card className="bg-white text-left rounded-2xl shadow-md w-60 mr-4 p-4">
    <div className="font-bold mb-1">Source Columns</div>
    <ul className="list-disc list-inside text-sm">
      <li>zcol_M1</li>
      <li>zcol_W1</li>
      <li>zcol_D1</li>
      <li>zcol_H4</li>
      <li>mfi_str_M1</li>
      <li>mfi_str_W1</li>
      <li>mfi_str_D1</li>
      <li>mfi_str_H4</li>
    </ul>
  </Card>
);

const SummaryBox = () => (
  <Card className="bg-white text-left rounded-2xl shadow-md w-60 mr-4 p-4 mt-4">
    <div className="font-bold mb-1">MFI Alignment</div>
    <ul className="list-disc list-inside text-sm mb-2">
      <li>M1: Bullish</li>
      <li>W1: Bullish</li>
      <li>D1: Bearish</li>
      <li>H4: Bearish</li>
    </ul>
    <div className="font-bold mb-1 mt-2">Zone Summary</div>
    <ul className="list-disc list-inside text-sm">
      <li>M1: green</li>
      <li>W1: red</li>
      <li>D1: gray</li>
      <li>H4: red</li>
    </ul>
  </Card>
);

export default function TrendDiagram() {
  return (
    <div className="flex justify-center p-6">
      <div className="flex flex-col justify-start">
        <InstrumentBox />
        <SourceBox />
        <SummaryBox />
      </div>
      <div className="flex flex-col items-center space-y-2">
        <TrendBox label="M1" trend="Bullish" mfi="++" zcol="green" />
        <Arrow />
        <TrendBox label="W1" trend="Bullish" mfi="--" zcol="red" />
        <Arrow />
        <TrendBox label="D1" trend="Bearish" mfi="-+" zcol="gray" />
        <Arrow />
        <TrendBox label="H4" trend="Bearish" mfi="--" zcol="red" />
      </div>
    </div>
  );
}
