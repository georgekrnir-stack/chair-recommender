"use client";

interface ChairCardProps {
  chair: {
    id: string;
    canonical_name: string;
    maker: string | null;
    price_range: string | null;
    is_recommendable: boolean;
    features: string[];
    pros: string[];
    cons: string[];
  };
  onToggleRecommendable?: (id: string, value: boolean) => void;
}

export default function ChairCard({ chair, onToggleRecommendable }: ChairCardProps) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <div>
          <h3 className="font-medium">{chair.canonical_name}</h3>
          {chair.maker && <p className="text-sm text-gray-500">{chair.maker}</p>}
        </div>
        <span
          className={`text-xs px-2 py-1 rounded ${
            chair.is_recommendable
              ? "bg-green-100 text-green-800"
              : "bg-gray-100 text-gray-600"
          }`}
        >
          {chair.is_recommendable ? "紹介可" : "要確認"}
        </span>
      </div>
      {chair.price_range && (
        <p className="text-sm text-gray-600 mb-2">価格帯: {chair.price_range}</p>
      )}
      {chair.features?.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {chair.features.map((f: string, i: number) => (
            <span key={i} className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded">
              {f}
            </span>
          ))}
        </div>
      )}
      {onToggleRecommendable && (
        <button
          onClick={() => onToggleRecommendable(chair.id, !chair.is_recommendable)}
          className="text-xs text-blue-600 hover:underline mt-2"
        >
          {chair.is_recommendable ? "要確認に戻す" : "紹介可にする"}
        </button>
      )}
    </div>
  );
}
