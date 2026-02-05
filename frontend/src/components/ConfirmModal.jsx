const ConfirmModal = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-12 max-w-xl w-full mx-4 border border-gray-200">
        <h3 className="text-2xl text-center mb-12 font-medium text-gray-800">
          Would you like to submit a review?
        </h3>
        <div className="flex justify-around items-center">
          <button
            onClick={() => {
              /* Xử lý Submit ở đây */ onClose();
            }}
            className="text-2xl font-bold hover:text-teal-600 transition-colors"
          >
            Yes
          </button>
          <button
            onClick={onClose}
            className="text-2xl font-bold hover:text-red-600 transition-colors"
          >
            No
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;
