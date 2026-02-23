import RecommendForm from "@/components/RecommendForm";

export default function HomePage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">椅子レコメンド</h2>
      <p className="text-gray-600 mb-6">
        公式LINEフォームの回答内容を貼り付けて、AIにおすすめの椅子を聞いてみましょう。
      </p>
      <RecommendForm />
    </div>
  );
}
