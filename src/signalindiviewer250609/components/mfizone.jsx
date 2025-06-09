import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowDown } from "lucide-react";

const LabelTag = ({ title }: { title: string }) => (
  <div className="text-[10px] text-gray-500 mb-1 font-medium uppercase tracking-wide">
    {title}
  </div>
);

const MFIBox = ({ label, mfi }: { label: string; mfi: string }) => {
  const mfiColor =
    mfi === "++" ? "bg-green-100" :
    mfi === "--" ? "bg-yellow-100" :
    mfi === "-+" ? "bg-red-100" :
    mfi === "+-" ? "bg-gray-100" : "bg-gray-50";

  return (
    <Card className={`${mfiColor} border text-center rounded-2xl shadow-md w-24`}>
      <CardContent className="p-2">
        <div className="font-bold text-base">{label}</div>
        <div className="text-sm font-medium">{mfi}</div>
      </CardContent>
    </Card>
  );
};

const ZoneBox = ({ label, zcol }: { label: string; zcol: string }) => {
  const zoneColor =
    zcol === "green" ? "bg-green-100" :
    zcol === "red" ? "bg-red-100" :
    zcol === "gray" ? "bg-gray-100" : "bg-white";

  return (
    <Card className={`${zoneColor} border text-center rounded-2xl shadow-md w-24`}>
      <CardContent className="p-2">
        <div className="font-bold text-base">{label}</div>
        <div className="text-sm font-medium text-gray-600">{zcol}</div>
      </CardContent>
    </Card>
  );
};

const TrendBox = ({ label, trend }: { label: string; trend: string }) => {
  const color =
    trend === "Bullish"
      ? "bg-green-100 border-green-400"
      : trend === "Bearish"
      ? "bg-red-100 border-red-400"
      : "bg-gray-100 border-gray-300";

  return (
    <Card className={`${color} border text-center rounded-2xl shadow-md w-24`}>
      <CardContent className="p-2">
        <div className="font-bold text-base">{label}</div>
        <div className="text-sm font-medium">{trend}</div>
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
  <Card className="bg-white text-left rounded-2xl shadow-md w-full p-3">
    <div className="font-bold text-base mb-1">Instrument</div>
    <div className="text-sm">NZD/CAD</div>
    <div className="text-xs text-gray-600 mt-1">Last H4 Close: 0.82734</div>
  </Card>
);

const SourceBox = () => (
  <Card className="bg-white text-left rounded-2xl shadow-md w-full p-3">
    <div className="font-bold text-[11px] mb-1">Source Columns</div>
    <ul className="list-disc list-inside text-[9px]">
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

const MFISummaryBox = () => (
  <Card className="bg-white text-left rounded-2xl shadow-md w-full p-3 mt-1">
    <div className="font-bold text-sm mb-1">MFI Alignment</div>
    <ul className="list-disc list-inside text-xs">
      <li>M1: Bullish</li>
      <li>W1: Bearish</li>
      <li>D1: Bearish</li>
      <li>H4: Bullish</li>
    </ul>
  </Card>
);

const ZoneSummaryBox = () => (
  <Card className="bg-white text-left rounded-2xl shadow-md w-full p-3 mt-1">
    <div className="font-bold text-sm mb-1">Zone Summary</div>
    <ul className="list-disc list-inside text-xs">
      <li>M1: red</li>
      <li>W1: gray</li>
      <li>D1: red</li>
      <li>H4: green</li>
    </ul>
  </Card>
);

const MetadataBox = () => (
  <Card className="bg-white text-left rounded-2xl shadow-md w-60 p-2 mr-4">
    <div className="space-y-2">
      <InstrumentBox />
      <SourceBox />
      <MFISummaryBox />
      <ZoneSummaryBox />
    </div>
  </Card>
);

const ColumnWrapper = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <Card className="bg-white text-center rounded-2xl shadow-md p-2 w-28" id={title}>
    <LabelTag title={title} />
    <div className="flex flex-col items-center space-y-2">
      {children}
    </div>
  </Card>
);

export default function TrendDiagram() {
  const timeframes = [
    { label: "M1", trend: "Bullish", mfi: "++", zcol: "red" },
    { label: "W1", trend: "Bearish", mfi: "-+", zcol: "gray" },
    { label: "D1", trend: "Bearish", mfi: "--", zcol: "red" },
    { label: "H4", trend: "Bullish", mfi: "++", zcol: "green" },
  ];

  return (
    <div className="flex justify-center p-6">
      <MetadataBox />
      <div className="flex flex-row space-x-4">
        <ColumnWrapper title="MFIZone">
          {timeframes.map((tf, idx) => (
            <React.Fragment key={tf.label}>
              <TrendBox label={tf.label} trend={tf.trend} />
              {idx < timeframes.length - 1 && <Arrow />}
            </React.Fragment>
          ))}
        </ColumnWrapper>
        <ColumnWrapper title="MFI">
          {timeframes.map((tf, idx) => (
            <React.Fragment key={tf.label}>
              <MFIBox label={tf.label} mfi={tf.mfi} />
              {idx < timeframes.length - 1 && <Arrow />}
            </React.Fragment>
          ))}
        </ColumnWrapper>
        <ColumnWrapper title="Zone">
          {timeframes.map((tf, idx) => (
            <React.Fragment key={tf.label}>
              <ZoneBox label={tf.label} zcol={tf.zcol} />
              {idx < timeframes.length - 1 && <Arrow />}
            </React.Fragment>
          ))}
        </ColumnWrapper>
      </div>
    </div>
  );
}
