import React from 'react';

interface FlowCardProps {
  title: string;
  description?: string;
  bgColorClass?: string; // Made optional, default can be applied
  icon?: React.ReactNode;
  children?: React.ReactNode;
  titleExtra?: React.ReactNode;
}

const FlowCard: React.FC<FlowCardProps> = ({ title, description, bgColorClass = 'bg-white', icon, children, titleExtra }) => {
  return (
    <div className={`rounded-xl shadow-lg ${bgColorClass} border border-gray-200`}>
      <div className="p-5 sm:p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-start">
            {icon && <div className="mr-4 text-gray-600 flex-shrink-0 w-8 h-8 flex items-center justify-center">{icon}</div>}
            <div>
              <h2 className="text-lg sm:text-xl font-semibold text-gray-800">{title}</h2>
              {description && <p className="text-xs sm:text-sm text-gray-500 mt-1">{description}</p>}
            </div>
          </div>
          {titleExtra && <div className="ml-4">{titleExtra}</div>}
        </div>
        {children && <div className="mt-4">{children}</div>}
      </div>
    </div>
  );
};

export default FlowCard;
